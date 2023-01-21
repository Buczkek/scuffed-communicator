#!/usr/bin/python

import sys as s



with open(s.argv[1]) as f:
    s = f.read()


d = dict ([tuple(l.split(": ")) for l in s.split("\n")])


print(d)