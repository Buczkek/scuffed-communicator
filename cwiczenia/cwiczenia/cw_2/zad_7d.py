lista = input().split()
lista = [int(x) for x in lista]

lista.sort()
print(lista)
wynik = []
wynik = [(lista[y], lista[x]) for x in range(0, len(lista)) for y in range(
    0, len(lista)) if x != y and lista[x] % lista[y] == 0]
wynik = set(wynik)

print(list(wynik))
print(len(wynik))
