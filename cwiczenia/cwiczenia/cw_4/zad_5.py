#!/usr/bin/python
from sys import argv, path

with open(argv[1]) as f1:
    with open(argv[2]) as f2:
        with open(argv[3], "w") as wyn:

            #print(f1, f2, wyn)

            for line in f1:
                if line not in f2:
                    print(line)

                    print(line, file=wyn, end="")
            f2.seek(0)
            for line in f2:
                if line not in f1:
                    print(line)
                    print(line, file=wyn, end="")
