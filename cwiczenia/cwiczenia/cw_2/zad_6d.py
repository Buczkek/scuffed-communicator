def czy_pierwsze(a):
    for x in range(2, int(a ** 0.5)+1):
        if(a % x == 0):
            return False
    return True


def gen_l_pierwszych(n):
    j = 2
    i = 0
    while i < n:
        if czy_pierwsze(j):
            i += 1
            yield j
        j += 1


pierwsze = [x for x in gen_l_pierwszych(15)]
print(pierwsze)
