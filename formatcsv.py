def wrap(x, y):
    final = map(list, zip(x, y))
    final = list(final)
    for i in list(final):
        i[0] += ","
        i[1] += "\n"

    return final


def list2string(item):
    a = ""
    for i in item:
        a += i[0]
        a += i[1]
    return a[:-2]


def fix(x):
    return x.split("\n")


x = fix('''0.21
0.51
0.87
1.03
1.26
1.46
1.81
2.15
2.44
2.78
2.95
3.78 ''')

y = fix('''1.2
10.6
31.2
61.6
96.8
131.6
167.6
201.4
212.1
213
204.8
174.2 ''')

filename = "cold_rolled.csv"
target = open(filename, 'w')

final = wrap(x, y)
final = list2string(final)

target.write(final)

target.close()
