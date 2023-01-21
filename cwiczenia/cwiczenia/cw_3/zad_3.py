class Liczba():
    lista = []

    def __init__(self, string: str) -> None:
        for l in string:
            self.lista.append(l)

    def wypisz(self):
        for l in self.lista:
            print(l, end="")
    def mnozenie_int(self, a:int):
        return a *int("".join(self.lista))



l = Liczba("111")

print(l.mnozenie_int(2))