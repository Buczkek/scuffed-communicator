n = int(input())

alfabet = [chr(x) for x in range (ord('a'), ord('z')+1, n)]

for l in alfabet:
    print (l, l.upper())