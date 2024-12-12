from PIL import Image, ImageDraw, ImageFont
from copy import deepcopy
import os, shutil
import subprocess

def ints(string):
	""" Extracts all integers from a string """
	nbr = None;
	neg = False;
	ints = [];
	for char in string:
		if char.isdigit():
			if nbr == None:
				nbr = 0;
			nbr = 10*nbr + int(char)
		elif nbr is not None:
			ints.append(-nbr if neg else nbr);
			nbr = None;
			neg = False;
		else:
			neg = char == '-';
			
	if nbr is not None:
		ints.append(-nbr if neg else nbr);

	return ints

with open('input.txt', 'r') as file:
	lines = file.read().strip().split("\n")

reports = [ints(line) for line in lines]

# keep a state of what to visualize.

# State: done (True/False/None, color whole line), report from line in text
# Whole state: [ok sum, fail sum, reports]
states = [ [None, None, [[None, report] for report in lines]] ]

def issafe(report):
	return (report == sorted(report) or report == sorted(report)[::-1]) and all([abs(x - y) >= 1 and abs(x - y) <= 3 for (x, y) in zip(report, report[1:])])

for (ri, report) in enumerate(reports):
	if issafe(report):
		# Immediately safe
		new = deepcopy(states[-1])
		new[2][ri][0] = True
		states.append(new)
	else:
		for i in range(len(report)):
			if issafe(report[:i] + report[i+1:]):
				new = deepcopy(states[-1])
				new[2][ri][0] = True
				new[2][ri][1] = " ".join(map(str, report[:i] + report[i+1:]))
				states.append(new)
				break
		else:
			new = deepcopy(states[-1])
			new[2][ri][0] = False
			states.append(new)

states.append(deepcopy(states[-1]))
states[-1][0] = states[-1][1] = 0

for ok, _ in states[-1][2]:
	new = deepcopy(states[-1])
	new[2].pop(0)
	if ok:
		new[0] += 1
	else:
		new[1] += 1
	states.append(new)

# Now just visualize everything!

def draw_state(state):
	width = 1000*2
	height = 666*2

	img = Image.new("RGB", (width, height), "black")
	draw = ImageDraw.Draw(img)

	# How much width and height to generate for each line?
	# Load the font
	try:
		font = ImageFont.truetype("arial.ttf", 12)  # Arial is common on most systems
		lfont = ImageFont.truetype("arial.ttf", 22)  # Arial is common on most systems
	except IOError:
		print("Could not find font")
		lfont = font = ImageFont.load_default()  # Fall back to default if Arial is not available

	line_width = width/11
	line_height = 13

	rows = height // (line_height + 1)

	if state[0] is not None:
		draw.text((0, 0), str(state[0]), fill="green", font=lfont)
		draw.text((line_width//2, 0), str(state[1]), fill="red", font=lfont)

	for i, (col, text) in enumerate(state[2]):
		if col is None:
			color = "white"
		elif col is True:
			color = "green"
		else:
			color = "red"
		row = (i + 2) % rows
		col = (i + 2) // rows
		draw.text((line_width*col, line_height*row), text, fill=color, font=font)

	return img


# Generate the frames
output_dir = "frames"
if os.path.exists(output_dir):
	shutil.rmtree(output_dir)

os.makedirs(output_dir, exist_ok=True)

for i, state in enumerate(states):
	print(f"gen frame {i}/{len(states)}")
	img = draw_state(state)
	img.save(f"{output_dir}/frame_{i:04d}.png")

# Now combine into a video
def gen_video(output_dir, framerate = 60):
	"""Generate a video from frames using ffmpeg."""
	name = "red-nosed-reports.mp4"
	ffmpeg_cmd = [
		"ffmpeg",
		"-framerate", str(framerate),
		"-i", f"{output_dir}/frame_%04d.png",
		"-pix_fmt", "yuv420p",
		name,
		"-y", 
	]
	subprocess.run(ffmpeg_cmd, check=True)
	print(f"output video saved as {name}")

gen_video(output_dir)

