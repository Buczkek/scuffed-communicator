s = """k1: w2
k2: w2
k3: w3"""


d = dict ([tuple(l.split(": ")) for l in s.split("\n")])


print(d)