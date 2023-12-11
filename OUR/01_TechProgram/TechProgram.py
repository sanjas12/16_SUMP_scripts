in_file = "in_TechProgram"
out_file = "out_TechProgram.xml"

list_cells = []

with open(in_file, 'r', encoding='utf-8') as f_in:
    for line in f_in.readlines():
        if line.startswith('#'):
            continue
        list_cells.append(tuple(line.strip().split(';')))

with open(out_file, 'w', encoding='utf-8') as f_out:
    for line in list_cells:
        f_out.write('\t\t\t<TechObject name="CycleInventOneRI_withoutUP" operatorsname="Администратор" repeat="true" '
                    'status="0" timestart="04/07/2022 17:29:41:761" timestop="04/07/2022 17:29:45:209">' + "\n")
        f_out.write(f'\t\t\t\t<Param xmlns:dt="urn:schemas-microsoft-com:datatypes" dt:dt="string" CellCoords="true" '
                    f'id="0">{line[0]};{line[1]}</Param>' + "\n")
        f_out.write(f'\t\t\t</TechObject>' + "\n")
