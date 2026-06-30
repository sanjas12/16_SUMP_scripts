from parser_service_area import MyParser


def main():
    file_in = "00_parser_service_area\data\ServiceArea.txt"
    my_data = MyParser(file_in)
    print(my_data)


if __name__ == "__main__":
    main()
