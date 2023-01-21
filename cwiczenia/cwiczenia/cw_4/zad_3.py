#!/usr/bin/python
from sys import argv

d = dict()

with open(argv[1]) as f:
    for line in f:
        line = line.strip()
        for word in line.split():
            if word in d:
                d[word] += 1

            else:
                d[word] = 1

print(d)
