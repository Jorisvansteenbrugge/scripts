string = """g16587.t1
g12560.t1
g8157.t1
g8150.t1
g8153.t1
g7830.t1
g7829.t1
g6815.t1
g8500.t1
g6203.t1
g7834.t1
g7820.t1"""

l = string.split("\n")
print("\n".join(sorted(list(set(l)))))