def odleglosc(p1, p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5


def odleglosc_punktow(punkty: list, kontrolny: tuple):
    result = []
    for p in punkty:
        result.append((odleglosc(p, kontrolny), p))
    result.sort()
    return result


p = [(2, 2), (30, 30), (0, 0), (3, 3), (4, 4)]

print(odleglosc_punktow(p, (1, 1)))
