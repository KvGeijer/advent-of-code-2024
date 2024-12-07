with open("input.txt", 'r') as f:
	lines = f.readlines()

def valid(acc, ints, target, conc_ok):
	if not ints:
		return acc == target
	else:
		return valid(acc * ints[0], ints[1:], target, conc_ok) \
			or valid(acc + ints[0], ints[1:], target, conc_ok) \
			or conc_ok and valid(int(str(acc) +  str(ints[0])), ints[1:], target, conc_ok)

for p2 in [False, True]:
	tot = 0
	for line in lines:
		(target, rest) = line.split(": ")
		target = int(target)
		ints = [int(c) for c in rest.split(' ')]
		if valid(ints[0], ints[1:], target, p2):
			tot += target
	print(tot)
	
