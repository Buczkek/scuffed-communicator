"""liczby = range (0, 20)

lista = [x*2 for x in liczby]


print(lista)

"""

"""def f1(n):
    def f2(m):
        return n - m
    return f2

res = f1(5)

print (res(10))"""


"""def fLog(x):
    return x > 5

def test(number, fun):
    if fun(number):
        print ("OK")
    else:
        print("ERR")"""

def generator(n):
    while n:
        print("generator stop %d" %n)
        yield n
        print ("Generator start %d" %n)
        n -=1

for x in generator(5):
    print (x)

gen = generator(1)
elem = next(gen, None)

while elem:
    print(elem)
    elem = next(gen, None)