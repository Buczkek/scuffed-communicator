from os import listdir

def gen_plikow(katalog, roz):
    lista = listdir(katalog)
    result = [x for x in lista if x.split('.')[-1] == roz]
    n = len(result) - 1
    i = 0
    while i < n:
        yield result[i]
        i += 1
    

for x in gen_plikow(None, "py"):
    print(x)
