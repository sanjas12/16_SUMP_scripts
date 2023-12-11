
import chardet
import configparser


class MyParser():
    def __init__(self, file_in="00_parser_service_area\data\ServiceArea_small.txt"):
        self.file_in = file_in
        self.file_out = '00_parser_service_area\data\out.txt'
        self.DISPLACEMENT = ''
        self.xdown = self.xup = self.ydown = self.yup = self.zdown = self.zup = self.Description = ''
        self.data = {}

    # def diagonal_parallelepiped(self, a0, a1, b0, b1, c0, c1):
    #     a = int(a1) - int(a0)
    #     b = int(b1) - int(b0)
    #     c = int(c1) - int(c0)
    #     print(a, b, c)
    #     return math.sqrt(a ** 2 + b ** 2 + c ** 2)


        # определение кодировки
        with open(self.file_in, 'rb') as f:
            raw_data = f.read(20000)
            encoding = chardet.detect(raw_data)['encoding']
        print('encoding:', encoding)

        config = configparser.RawConfigParser()
        # вывод название секции в регистре в каком и было в ini файле. первый способ
        # config.optionxform = lambda option: option
        # второй способ
        config.optionxform = str

        config.read(self.file_in, encoding=encoding)

        # print(len(config.sections()))

        global_param = config.sections()[0]
        self.DISPLACEMENT = int(config[global_param]['Displacement'])

        for name_zone in config.sections():
            if name_zone == 'Global_Parameters':
                continue
            else:
                # print('_', name_zone)
                if name_zone in self.data:
                    pass
                else:
                    self.data.setdefault(name_zone, {})
                    self.data[name_zone].setdefault('Xup', config[name_zone]['Xup'])
                    self.data[name_zone].setdefault('Xdown', config[name_zone]['Xdown'])
                    self.data[name_zone].setdefault('Yup', config[name_zone]['Yup'])
                    self.data[name_zone].setdefault('Ydown', config[name_zone]['Ydown'])
                    self.data[name_zone].setdefault('Zup', config[name_zone]['Zup'])
                    self.data[name_zone].setdefault('Zdown', config[name_zone]['Zdown'])
                    self.data[name_zone].setdefault('Description', config[name_zone]['Description'])

        # with open(self.file_out, 'a') as f:
        #     f.write('test1')
        #     f.write('\n')

        # return xdown, xup, ydown, yup, zdown, zup, self.Short_Description

    def get_data(self):
        return self.data

    def __str__(self):
        self.result = ""
        for name_subzone, v in self.data.items():
            self.result += name_subzone
            self.result += "\n"
            self.result += "".join(f'{a:<20}:{b:>6}\n' for a, b in v.items())
        return self.result


def main():
    file_in = "00_parser_service_area\data\ServiceArea_small.txt"
    my_data = MyParser(file_in)
    print(my_data)
    # data = {'Displacement': my_data.DISPLACEMENT}
    # for zone in my_data.get_data():
    #     data = zone
    # print('длина словаря: ', len(data))


if __name__ == '__main__':
    main()
