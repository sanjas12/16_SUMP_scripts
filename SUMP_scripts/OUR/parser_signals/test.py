col_type = ['bit']*20

print(col_type)

col_adr = ['']*20
col_adr[0] = '32020.0'
col_adr[10] = '32021.0'
print(col_adr)


# print(str(int(col_adr[0][-1:])+1))
for _ in range(len(col_type)):
    if col_type[_] == 'bit' and len(col_adr[_]) < 1:
        col_adr[_] = col_adr[_-1][:5] + '.' + str(int(col_adr[_-1].split('.')[-1])+1)


for _ in range(len(col_adr)):
    print(col_type[_], col_adr[_])