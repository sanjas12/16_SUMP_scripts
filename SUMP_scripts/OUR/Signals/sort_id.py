import configparser
import chardet


file_in = 'Data\Signals_2.ini'
file_out = file_in[:-4] + '_out' + file_in[-4:]

# определение кодировки
with open(file_in, 'rb') as f:
    raw_data = f.read(20000)
    encoding = chardet.detect(raw_data)['encoding']

# необходимо использовать именно raw
config_in = configparser.RawConfigParser(inline_comment_prefixes=('//', '\\'))
config_in.optionxform = str  # для сохранения регистра
# config_in.optionxform = lambda option: option
config_out = configparser.RawConfigParser()
config_in.optionxform = str  # для сохранения регистра


config_in.read(file_in, encoding=encoding)


# вывод всех значений и ключей
# print(config_in.items(section))

sortable_sections = [s for s in config_in if 'Id' in config_in[s]]
other_sections = [s for s in config_in if 'Id' not in config_in[s]]

for section in other_sections:
    config_out[section] = config_in[section]

for section in sorted(sortable_sections, key=lambda sec: config_in[sec].getint('Id')):

    config_out[section] = config_in[section]

# print(config_in.sections())
# print(config_out.sections())


with open(file_out, 'w', encoding='UTF-8-sig') as file_config_out:
    config_out.write(file_config_out)



#TODO
# import chardet
