import os.path

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read().splitlines()

x, y, z = 0, 0, 0
for inst in data:
    command, num = inst.split(" ")
    match command:
        case "forward":
            x += int(num)
            y += int(num) * z
        case "up":
            z -= int(num)
        case "down":
            z += int(num)
print("Part 1:", x*z)
print("Part 2:", x*y)
