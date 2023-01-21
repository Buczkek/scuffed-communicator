#!/usr/bin/python
from sys import argv


def encrypt(string: str, k: int):
    result = ''
    for l in string:
        if l in " /.,;:'[]-=\\\n":
            result += l
            continue
        if ord(l) > 122 - k:
            result += chr(ord(l) + k - 26)
        else:
            result += chr(ord(l) + k)

    return result


with open(argv[1]) as f:
    s = f.read()


with open(argv[2], 'w') as f:
    print(encrypt(s, 3), file=f)
