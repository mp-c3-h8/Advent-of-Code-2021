import os.path
from timeit import default_timer as timer

def hex_to_binary(hexa: str) -> str:
    res = ""
    for c in hexa:
        bina = bin(int(c, 16))[2:].zfill(4)
        res += bina
    return res


s = timer()


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

binary = hex_to_binary(data)
print("Part 1:", binary)

e = timer()
print("time:", e - s)
