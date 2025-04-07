from typing import NamedTuple, List

in_file = "in_TechProgram"
out_file = "out_TechProgram.xml"
encoding='utf-8'
default_time = '00/00/0000 00:00:00:000'
name_program = 'Инвентаризация в БВ2'

class Cell(NamedTuple):
    bridge: str  # Пример типа (можно заменить на нужный)
    trolley: str  # Пример типа (можно заменить на нужный)


cells:  List[Cell] = []

with open(in_file, 'r', encoding=encoding) as f_in:
    for line in f_in.readlines():
        if line.startswith('#'):
            continue
        cell = Cell(*tuple(line.strip().split(';')))
        cells.append(cell)
# print(list_cells)
with open(out_file, 'w', encoding=encoding) as f_out:
    f_out.write(f'\t<TechProgram name="1. {name_program}" type="1">' + "\n")
    f_out.write(f'\t\t<DisplayedName xmlns:dt="urn:schemas-microsoft-com:datatypes"' + 
                f'dt:dt="string">{name_program}</DisplayedName>' + "\n")
    f_out.write(f'\t\t<Description xmlns:dt="urn:schemas-microsoft-com:datatypes"' +
                f'dt:dt="string">{name_program}</Description>' + "\n")
    for cell in cells:
        f_out.write(f'\t\t\t<TechObject name="CycleInventOneRI_withoutUP" operatorsname="Администратор" repeat="true" ' + 
                    f'status="0" timestart="{default_time}" timestop="{default_time}">' + "\n")
        f_out.write(f'\t\t\t\t<Param xmlns:dt="urn:schemas-microsoft-com:datatypes" dt:dt="string" CellCoords="true" ' + 
                    f'id="0">{cell.bridge};{cell.trolley}</Param>' + "\n")
        f_out.write(f'\t\t\t</TechObject>' + "\n")

    f_out.write(f'\t<TechProgram>' + "\n")
