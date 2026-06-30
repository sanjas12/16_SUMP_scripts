import zipfile
import xml.dom.minidom

document = zipfile.ZipFile('31.docx')
# print(document)

uglyXml = xml.dom.minidom.parseString(document.read('word/document.xml')).toprettyxml(indent='  ')

def teg_parser(raw_string):
    start_teg = '<w:tbl>'
    end_teg = "</w:tbl>"
    start_index = raw_string.find(start_teg)
    end_index = raw_string.find(end_teg)
    return raw_string[start_index:end_index]

if __name__ == "__main__":
    print(len(teg_parser(uglyXml)))