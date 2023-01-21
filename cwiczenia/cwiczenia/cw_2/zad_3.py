def fbool(a):
    return a > 5

def f(lista: list, f):
    return [x for x in lista if f(x)]

print(f([1,2,3,4,5,6,7,8,9,10], fbool))

