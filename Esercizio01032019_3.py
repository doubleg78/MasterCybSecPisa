def trovaMCD(a,b):
    while b != 0:
        a, b = b, a % b
        print a, b
    return a

x = int(raw_input('Numero x: \n'))
y = int(raw_input('Numero y: \n'))
print trovaMCD(x,y)