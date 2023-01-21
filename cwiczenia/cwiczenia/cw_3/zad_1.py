class Liczby_zespolone():
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __add__(self, other):
        return Liczby_zespolone(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Liczby_zespolone(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Liczby_zespolone(self.x * other.x + self.y * other.y, self.x * other.y + self.x * other.y)

    def __truediv__(self, other):
        return Liczby_zespolone((self.x * other.x + self.y * other.y) /
                                (other.x**2 + other.y**2),
                                (self.y * other.x - self.x * other.y) /
                                (other.x**2 + other.y**2))

    def __eq__(self, other):
        return self.x == self.x and self.y == self.x

    def __lt__(self, other):
        return self.x < self.x and self.y < self.x

    def __gt__(self, other):
        return self.x > self.x and self.y > self.x

    def modul(self):
        return (self.x**2 + self.y**2)**0.5


    def __str__(self) -> str:
        return (self.x + "+i" + self.y)
