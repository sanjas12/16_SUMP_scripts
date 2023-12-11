file = 'test.csv'

col_type = []
col_adre = []
col_name = []

type_sig = {'dint': 'int32', 'bit': 'bit', 'real': 'float'}

with open(file) as f:
    for line in f:
        _ = line.split(';')
        # _[0]       _[3]                _[4]
        # 'Тип данных', 'Адрес',   'Наименование сигнала',
        if _[0] in type_sig.keys() and len(_[4]) > 1:
            if _[0] == 'dint':
                col_type.append('int32')
            elif _[0] == 'real':
                col_type.append('float')
            else:
                col_type.append(_[0])
            col_adre.append(_[3])
            col_name.append(_[4].replace('"', ''))

# добавление адреса если его нет
for _ in range(len(col_type)):
    if col_type[_] == 'bit' and len(col_adre[_]) < 1:
        col_adre[_] = col_adre[_ - 1][:5] + '.' + str(int(col_adre[_ - 1].split('.')[-1]) + 1)

# создание XML
xml_name = 'out_script.xml'
with open(xml_name, 'w', encoding="utf-8") as xml_out:
    xml_out.write('\t'*3 + '<group readFunctionCode="3" hostId="0">' + '\n')
    for _ in range(len(col_name)):
        # print(f'<signal address= "{col_adre[_]}" icsId="{_}" name="{col_name[_]}" type="{col_type[_]}" />')
        xml_out.write('\t'*4 + '<signal address="' + str(col_adre[_]) + '" icsId="' + str(_) + '" name="' +
                      str(col_name[_]) + '" type="' + str(col_type[_]) + '" />' + '\n')
