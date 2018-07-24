def diff(first, second):
    second = set(second)
    return [item for item in first if item not in second]


a = [['a','b','c'], ['1','2','3'], ['a','b','z']]
b = [[i[0],i[1]] for i in a]
c = [i[2] for i in a]
print('a:', a)
print('b:', b)
new_list = []
for i in b:
    for j in a:
        if i[0] == j[0]:
            temp = []
            if i[0] not in [x[0] for x in new_list]:
                temp.append(i + diff(j,i))
            else:
                temp.append(diff(j,i))






