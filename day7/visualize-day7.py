with open("input.txt", 'r') as f:
	lines = f.readlines()

def valid(ints, target, p2):
	if res := valid_rec(ints[0], ints[1:], target, p2):
		res.append(str(ints[0]))
		print(f"Original {ints}, solved {' '.join(reversed(res))}")
		return " ".join(res)
	else:
		return None
		
def valid_rec(acc, ints, target, conc_ok):
	if not ints:
		if acc == target:
			return [""]
		else:
			return None
	elif (res := valid_rec(acc * ints[0], ints[1:], target, conc_ok)) is not None:
		res.append(str(ints[0]))
		res.append('*')
		return res
	elif (res := valid_rec(acc + ints[0], ints[1:], target, conc_ok)) is not None:
		res.append(str(ints[0]))
		res.append('+')
		return res
	elif conc_ok and (res := valid_rec(int(str(acc) +  str(ints[0])), ints[1:], target, conc_ok)) is not None:
		res.append(str(ints[0]))
		res.append('++')
		return res
	else:
		return None

for p2 in [False, True]:
	tot = 0
	for line in lines:
		(target, rest) = line.split(": ")
		target = int(target)
		ints = [int(c) for c in rest.split(' ')]
		if valid(ints, target, p2):
			tot += target
	print(tot)
	
