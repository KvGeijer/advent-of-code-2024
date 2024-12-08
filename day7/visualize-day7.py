import pyray as pr

with open("input.txt", 'r') as f:
	lines = f.readlines()

# Old functions that return the final string
# def valid(ints, target, p2):
# 	if res := valid_rec(ints[0], ints[1:], target, p2):
# 		res.append(str(ints[0]))
# 		print(f"Original {ints}, solved {' '.join(reversed(res))}")
# 		return " ".join(res)
# 	else:
# 		return None
		
# def valid_rec(acc, ints, target, conc_ok):
# 	if not ints:
# 		if acc == target:
# 			return [""]
# 		else:
# 			return None
# 	elif (res := valid_rec(acc * ints[0], ints[1:], target, conc_ok)) is not None:
# 		res.append(str(ints[0]))
# 		res.append('*')
# 		return res
# 	elif (res := valid_rec(acc + ints[0], ints[1:], target, conc_ok)) is not None:
# 		res.append(str(ints[0]))
# 		res.append('+')
# 		return res
# 	elif conc_ok and (res := valid_rec(int(str(acc) +  str(ints[0])), ints[1:], target, conc_ok)) is not None:
# 		res.append(str(ints[0]))
# 		res.append('++')
# 		return res
# 	else:
# 		return None

# New functions that return all intermediate strings tried
def valid(ints, target):
	tries = []
	return (valid_rec(ints[0], str(ints[0]), ints[1:], target, tries), target, tries, "   ".join(ints))
		
def valid_rec(acc, acc_str, ints, target, tries):
	if not ints:
		tries.append((acc, acc_str))
		return acc == target
	elif valid_rec(acc * ints[0], acc_str + f" * {ints[0]}", ints[1:], target, tries):
		return True
	elif valid_rec(acc + ints[0], acc_str + f" + {ints[0]}", ints[1:], target, tries):
		return True
	else:
		return False

input = []
for line in lines:
	(target, rest) = line.split(": ")
	target = int(target)
	ints = [int(c) for c in rest.split(' ')]
	input.append((target, ints))

processes = []
for (target, ints) in sorted(input, reverse = True, key = lambda t: len(t[1]))[:20]:
	processes.append(valid(ints, target))

	
# Visualize the frames
frame = 0
done = False
while not done or frame <= len(processes):
	done = True
	for (pi, (valid, target, tries, start_str)) in enumerate(processes):
		state_ind = frame - pi - 1
		if state_ind >= len(tries) - 1: 
			# Print the final state
			if valid:
				# Show it in green, and that it equals
				pass
			else:
				# Show it in red, and that it does not equal
				pass
		elif state_ind >= 0
			done = False
			# Show a normal intermediate state
			(acc, acc_str) = tries[state_ind]
			# Print acc_str att correct offset in white, showing how acc compares to target
		else:
			# Just show the starting string in white, and the target
			pass

	frame += 1

# Done
