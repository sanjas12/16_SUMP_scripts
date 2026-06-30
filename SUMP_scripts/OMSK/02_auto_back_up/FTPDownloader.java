import org.apache.commons.net.ftp.FTP;
import org.apache.commons.net.ftp.FTPClient;
import org.apache.commons.net.ftp.FTPReply;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.text.SimpleDateFormat;
import java.util.Date;

public class FTPDownloader {

    // Настройки
    private static final String FTP_SERVER1 = "192.168.3.93";
    private static final String FTP_SERVER2 = "192.168.3.92";
    private static final String FTP_USER = "rs_pdu";
    private static final String FTP_PASS = "rs_pdu";
    private static final String REMOTE_PATH = "/home/rs_pdu/mpux/data";
    private static final String LOCAL_BASE_PATH = "C:\\back_up";
    private static final long INTERVAL = 8 * 60 * 60 * 1000; // 8 часов в миллисекундах
    private static final long INITIAL_DELAY = 0; // Задержка перед первым скачиванием (в миллисекундах)

    // Логирование
    private static void log(String message) {
        String timestamp = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(new Date());
        System.out.println("[" + timestamp + "] " + message);
    }

    // Создание папки для скачивания
    private static String createDownloadFolder() {
        String timestamp = new SimpleDateFormat("yyyy-MM-dd_HH-mm-ss").format(new Date());
        String downloadFolder = LOCAL_BASE_PATH + File.separator + timestamp;
        new File(downloadFolder).mkdirs();
        new File(downloadFolder + File.separator + "us_1(93)").mkdirs();
        new File(downloadFolder + File.separator + "us_2(92)").mkdirs();
        log("Создана папка для скачивания: " + downloadFolder);
        return downloadFolder;
    }

    // Скачивание файлов с FTP-сервера
    private static void downloadFTPFiles(String server, String user, String password, String remotePath, String localPath) {
        FTPClient ftpClient = new FTPClient();
        try {
            log("Подключение к " + server + "...");
            ftpClient.connect(server);
            ftpClient.login(user, password);

            int replyCode = ftpClient.getReplyCode();
            if (!FTPReply.isPositiveCompletion(replyCode)) {
                log("Ошибка подключения к " + server + ": " + replyCode);
                return;
            }

            ftpClient.enterLocalPassiveMode(); // Пассивный режим
            ftpClient.setFileType(FTP.BINARY_FILE_TYPE);

            // Переход в удаленную папку
            ftpClient.changeWorkingDirectory(remotePath);

            // Получение списка файлов
            String[] files = ftpClient.listNames();
            if (files == null || files.length == 0) {
                log("Нет файлов для скачивания на " + server);
                return;
            }

            // Скачивание файлов
            for (String file : files) {
                String localFilePath = localPath + File.separator + file;
                log("Скачивание " + file + " в " + localFilePath);
                try (OutputStream outputStream = new FileOutputStream(localFilePath)) {
                    ftpClient.retrieveFile(file, outputStream);
                }
            }

            log("Скачивание с " + server + " завершено.");
        } catch (IOException e) {
            log("Ошибка при скачивании с " + server + ": " + e.getMessage());
        } finally {
            try {
                if (ftpClient.isConnected()) {
                    ftpClient.logout();
                    ftpClient.disconnect();
                }
            } catch (IOException e) {
                log("Ошибка при отключении от " + server + ": " + e.getMessage());
            }
        }
    }

    // Ожидание с выводом оставшегося времени
    private static void wait(long millis) {
        long endTime = System.currentTimeMillis() + millis;
        while (System.currentTimeMillis() < endTime) {
            long remaining = (endTime - System.currentTimeMillis()) / 1000;
            long hours = remaining / 3600;
            long minutes = (remaining % 3600) / 60;
            long seconds = remaining % 60;
            log("Ожидание следующего скачивания: " + hours + " часов " + minutes + " минут " + seconds + " секунд");
            try {
                Thread.sleep(1000); // Спим 1 секунду
            } catch (InterruptedException e) {
                log("Ошибка при ожидании: " + e.getMessage());
            }
        }
    }

    // Основной метод
    public static void main(String[] args) {
        // Задержка перед первым скачиванием
        if (INITIAL_DELAY > 0) {
            log("Ожидание перед первым скачиванием: " + INITIAL_DELAY + " миллисекунд");
            try {
                Thread.sleep(INITIAL_DELAY);
            } catch (InterruptedException e) {
                log("Ошибка при ожидании: " + e.getMessage());
            }
        }

        // Основной цикл
        while (true) {
            // Создание папки для скачивания
            String downloadFolder = createDownloadFolder();

            // Скачивание с первого сервера
            downloadFTPFiles(FTP_SERVER1, FTP_USER, FTP_PASS, REMOTE_PATH, downloadFolder + File.separator + "us_1(93)");

            // Скачивание с второго сервера
            downloadFTPFiles(FTP_SERVER2, FTP_USER, FTP_PASS, REMOTE_PATH, downloadFolder + File.separator + "us_2(92)");

            // Ожидание до следующего скачивания
            wait(INTERVAL);
        }
    }
}