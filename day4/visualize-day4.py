import random
import pyray as pr
import time

with open("input.txt", 'r') as f:
    mat = {}
    for (i, line) in enumerate(f.readlines()):
        for (j, c) in enumerate(line):
            mat[(i, j)] = c

# Only Visualize part 2
search = ("MAS", "SAM")
xs = []

# Iterate in a random order is nice for visualizations :D
for (row, col) in random.sample(list(mat.keys()), len(mat)):
    down_right = "".join(mat.get(
        (row + o, col + o), '.') for o in range(-1, 2))
    down_left = "".join(mat.get(
        (row + o, col - o), '.') for o in range(-1, 2))

    if down_right in search and down_left in search:
        # Add to solution
        xs.append((row, col))



default_color = pr.GRAY
middle_color = pr.RED
outer_color = pr.GREEN

with open("input.txt", 'r') as f:
    input_lines = list(f.read().strip().split("\n"))

colored = [[[c, default_color] for c in line] for line in input_lines]

cols = len(input_lines[0])
rows = len(input_lines)

font_size = 16
char_width = font_size
line_height = 2 + font_size

# Initialize the window
width = 0 + char_width*cols
height = 0 + line_height*rows
pr.init_window(width, height, "Ceres Search")

# Set target FPS
pr.set_target_fps(20)

def draw_frame(colored):
    pr.clear_background(pr.BLACK)
    text_x = 1
    text_y = 1
    for line in colored:
        for (char, color) in line:
            pr.draw_text(char, text_x, text_y, font_size, color)
            text_x += char_width
        text_y += line_height
        text_x = 1

    pr.end_drawing()
            
    
draw_frame(colored)
time.sleep(3) # Time to start recording

for (i, (rx, cx)) in enumerate(xs, 1):
    # colored[rx][cx] = [str(i), middle_color]
    colored[rx][cx][1] = middle_color
    draw_frame(colored)
    for (ro, co) in ((-1, -1), (-1, 1), (1, -1), (1, 1)):
        colored[rx+ro][cx+co][1] = outer_color
    draw_frame(colored)
    
# Time to stop recording
print("DONEDODONTONDESNDOSNDOSNDERSNDOND")
time.sleep(10)
pr.close_window()

