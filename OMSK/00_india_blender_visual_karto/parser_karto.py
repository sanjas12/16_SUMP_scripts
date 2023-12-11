import chardet


class MyParserKarto:
    def __init__(self, file_in):
        self.file_out = 'D:\sanja\My_Work\Python\\16_SUMP_scripts\india\data\out.txt'
        self.DISPLACEMENT = ''
        self.x1 = self.x2 = self.y1 = self.y2 = self.z1 = self.z2 = ''
        self.data = {}

        # определение кодировки
        with open(file_in, 'rb') as f:
            raw_data = f.read(20000)
            encoding = chardet.detect(raw_data)['encoding']
        # print('encoding:', encoding)

        with open(file_in, 'r', encoding=encoding) as f:
            for line in f:
                if line.startswith("//"):
                    continue
                _, self.x1, self.y1, self.z1, self.x2, self.y2, self.z2, *_, name_subzone = line.split()
                # print("name subzone: ", name_subzone)
                if name_subzone not in self.data and name_subzone:
                    self.data.setdefault(name_subzone, {})
                    self.data[name_subzone].setdefault('X1', int(self.x1))
                    self.data[name_subzone].setdefault('X2', int(self.x2))
                    self.data[name_subzone].setdefault('Y1', int(self.y1))
                    self.data[name_subzone].setdefault('Y2', int(self.y2))
                    self.data[name_subzone].setdefault('Z1', int(self.z1))
                    self.data[name_subzone].setdefault('Z2', int(self.z2))

    def get_data(self):
        return self.data

    def __str__(self):
        self.result = ""
        for name_subzone, v in self.data.items():
            self.result += name_subzone
            self.result += "\n"
            self.result += "".join(f'{a:>20}:{b:>6}\n' for a, b in v.items())
        return self.result


def main():
    file_in = "D:\sanja\My_Work\Python\\16_SUMP_scripts\india\data\karto.txt"
    my_data = MyParserKarto(file_in)
    print(my_data.get_data()["Core"])
    # print(my_data)


if __name__ == '__main__':
    main()
