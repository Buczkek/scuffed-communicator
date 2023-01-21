n = int(input('Podaj n: '))
lista = []
for i in range(n):
    lista.append(input())
lista.sort()
print(lista)

mini, maxi = input('podaj min i max:').split()

for x in lista:
    if x >= mini and x <= maxi:
        print(x)