file = open("test", "r")
instructions = []
temp = []
for line in file:
	line = line.replace(" ", "")
	line = line.replace("        ", "")
	if line[0] != "#":
		temp.append(line)
	if line == "\n":
		if len(temp) >= 2:
			instructions.append(temp)

		temp = []


for ins in instructions:
	val1 = ins[0][ins[0].find("==")+2:ins[0].find(":")]
	val2 = ins[1][ins[1].find("=")+1:ins[1].find("\n")]
	print("elif color ==", val2,":")
	print("	interval = ", val1)
	print()

file.close()
