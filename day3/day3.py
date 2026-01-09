import os.path

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()


report = [[int(n) for n in row] for row in data.splitlines()]

gamma_rate_bin = "".join("1" if sum(col) > len(report)/2 else "0" for col in zip(*report))
epsilon_rate_bin = "".join("1" if c == "0" else "0" for c in gamma_rate_bin)


print("Part 1:", int(gamma_rate_bin, 2)*int(epsilon_rate_bin, 2))
