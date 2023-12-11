import re
import os
import zipfile
import xml.dom.minidom
import glob
import teg_parser

doc_name = glob.glob('*.doc')

document = zipfile.ZipFile('31.docx')
raw = 'out_raw.xml'
first_re = 'out_first_re.xml'

# запись текста из ДОКА в файл
def write_file(string, file):
    with open(file, 'w', encoding="utf-8") as f:
        for i, _ in enumerate(string):
            f.write(str(_) + '\n')

# RAW
text_RAW = xml.dom.minidom.parseString(document.read('word/document.xml')).toprettyxml(indent='  ')
print('количество строк RAW:', '\t'*2, len(text_RAW))


text_TEG = teg_parser.teg_parser(text_RAW)
print('количество строк TEG:', '\t'*2, len(text_TEG))

# RE_1
text_re_1 = re.findall('\<w:t>(.*)\<', text_TEG)
print('количество строк RE-first:', '\t', len(text_re_1))

# RE_2
text_re_2 = re.findall('\)+$', text_re_1)
print('количество строк RE-second:', '\t', len(text_re_2))


# запись RE-fisrt из RAW-текста в файл
with open(first_re, 'w', encoding="utf-8") as csv_out:
    for i, _ in enumerate(text_re_1):
        # print(i)
        csv_out.write(str(_))

upper_letter = ('А', 'Б', 'У', 'Т', 'Н')

# форматирование строк
for i, _ in enumerate(text_re_1):
    # print(i)
    #                           первая буква 1 элемента ЗАГЛАВНАЯ          первая буква 2 элемента НЕ заглавная
    if i < len(text_re_1) and str(_)[0].startswith(upper_letter) and not(str(text_re_1[i + 1])[0].startswith(upper_letter)):
        remove_item = text_re_1.pop(i+1)
        text_re_1[i] = str(text_re_1[i])+str(remove_item)
print('количество строк после формотирования:', len(text_re_1))



# count_block = text_in_doc.count('если выполняются следующие')
count_block = 181
# print('количество блокировок:', count_block)



# создание XML
xml_name = 'PermissionVariablesBlocking.xml'
with open(xml_name, 'w', encoding="utf-8") as xml_out:
    fdfs = '''<?xml version="1.0" encoding="utf-16"?>
<PermissionVariables>

  <!--
    #########################################################################
    Условия формирования блокировок и защит
    #########################################################################
  --> 
    '''
    xml_out.write(fdfs + '\n')

    for _ in range(count_block):
        text_01 = '<Variable name="bBlocking'
        text_02 = '">'
        xml_out.write(text_01 + str(_+1) + text_02 + '\n')
        xml_out.write('Тело блокировки' + '\n')
        xml_out.write('</Variable>' + '\n'*2)
    xml_out.write('\n')

    for _ in range(count_block):
        text_01 = '<Variable category="Blocking" id="'
        text_02 = '"> bBlocking'
        text_03 = ' </Variable>'
        xml_out.write(text_01 + str(_+1) + text_02 + str(_+1) + text_03 + '\n')
    xml_out.write('\n')

    xml_out.write('< / PermissionVariables >' + '\n')
