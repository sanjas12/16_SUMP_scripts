import os
from india_blender_visual_karto.parser_karto import MyParserKarto


def main():
    file = "\data\karto.txt"
    cur_dir = os.getcwd()
    file_in = cur_dir + file
    data = MyParserKarto(file_in)
    key = "Core"
    print(key, data.get_data()[key])


if __name__ == '__main__':
    main()
