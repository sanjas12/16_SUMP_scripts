data = {2: None}
a = 2
if a in data:
    data.setdefault(a)
    data[a] = 221
else:
    data[a] = 21
# print(data.setdefault(a))

data[2] = (1, 2)
data[2] = {}
data[2].setdefault(1,2)
data[2].setdefault(3,4)

print(data)