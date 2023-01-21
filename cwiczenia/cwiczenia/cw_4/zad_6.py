name = input()

width = int(input())

with open(name) as f:
    s = f.read()
    print(s)
    for l in s:
        print(l)
        print(l[width].strip().center(width))