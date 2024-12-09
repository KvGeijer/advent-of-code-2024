import itertools
import time
import pyray as pr

mat = dict()
with open("input.txt") as f:
    for (rowi, row) in enumerate(f.readlines()):
        for (coli, c) in enumerate(row.strip()):
            mat[(rowi, coli)] = c

freqs = [freq for freq in set(mat.values()) if freq != '.']


def vadd(x, y):
    return (x[0] + y[0], x[1] + y[1])


def vsub(x, y):
    return (x[0] - y[0], x[1] - y[1])


freq_poss = []
for freq in freqs:
    poss = []
    # We want to solve one freq at a time for the visualization
    for (pos, freq1) in mat.items():
        if freq1 != freq:
            continue
        poss.append(pos)

    freq_poss.append((freq, poss))

# List per freq, one entry per each combination of positions, where the entry is first a the line, and then all positions, in order, two by two
found = set()
steps = []
for (freq, poss) in freq_poss:
    freq_steps = []
    for pos1, pos2 in itertools.combinations(poss, 2):
        diff = vsub(pos1, pos2)
        antinodes = []

        while pos1 in mat.keys() or pos2 in mat.keys():
            if pos1 in mat.keys() and pos2 in mat.keys():
                found.add(pos1)
                found.add(pos2)
                antinodes.append((pos1, pos2))
            elif pos1 in mat.keys():
                found.add(pos1)
                antinodes.append((pos1,))
            elif pos2 in mat.keys():
                found.add(pos2)
                antinodes.append((pos2,))

            pos1 = vadd(pos1, diff)
            pos2 = vsub(pos2, diff)

        freq_steps.append(((pos1, pos2), antinodes))
    steps.append((freq, freq_steps))

# Answer to puzzle
# print(len(found))

# Colors for the different frequencies
colors = [
    pr.Color(255, 99, 71, 255),    # Tomato
    pr.Color(144, 238, 144, 255),  # Light Green
    pr.Color(173, 216, 230, 255),  # Light Blue
    pr.Color(255, 182, 193, 255),  # Light Pink
    pr.Color(255, 215, 0, 255),   # Gold
    pr.Color(72, 61, 139, 255),   # Dark Slate Blue
    pr.Color(255, 69, 0, 255),    # Orange Red
    pr.Color(124, 252, 0, 255),   # Lawn Green
    pr.Color(30, 144, 255, 255),  # Dodger Blue
    pr.Color(221, 160, 221, 255),  # Plum
    pr.Color(255, 140, 0, 255),   # Dark Orange
    pr.Color(102, 205, 170, 255),  # Medium Aquamarine
    pr.Color(70, 130, 180, 255),  # Steel Blue
    pr.Color(255, 20, 147, 255),  # Deep Pink
    pr.Color(128, 128, 0, 255),   # Olive
    pr.Color(135, 206, 250, 255),  # Light Sky Blue
    pr.Color(199, 21, 133, 255),  # Medium Violet Red
    pr.Color(238, 130, 238, 255),  # Violet
    pr.Color(0, 255, 127, 255),   # Spring Green
    pr.Color(65, 105, 225, 255),  # Royal Blue
    pr.Color(210, 105, 30, 255),  # Chocolate
    pr.Color(127, 255, 0, 255),   # Chartreuse
    pr.Color(123, 104, 238, 255),  # Medium Slate Blue
    pr.Color(139, 0, 139, 255),   # Dark Magenta
    pr.Color(0, 250, 154, 255),   # Medium Spring Green
    pr.Color(72, 209, 204, 255),  # Medium Turquoise
    pr.Color(255, 160, 122, 255),  # Light Salmon
    pr.Color(46, 139, 87, 255),   # Sea Green
    pr.Color(176, 224, 230, 255),  # Powder Blue
    pr.Color(255, 228, 181, 255),  # Moccasin
    pr.Color(205, 133, 63, 255),  # Peru
    pr.Color(240, 128, 128, 255),  # Light Coral
    pr.Color(153, 50, 204, 255),  # Dark Orchid
    pr.Color(255, 250, 205, 255),  # Lemon Chiffon
    pr.Color(60, 179, 113, 255),  # Medium Sea Green
    pr.Color(95, 158, 160, 255),  # Cadet Blue
    pr.Color(244, 164, 96, 255),  # Sandy Brown
]

antennas = []
for (pos, freq) in mat.items():
    if freq == '.':
        continue

    ind = freqs.index(freq)
    color = colors[ind]
    antennas.append((pos, freq, color))


def draw_line(poss, color):
    ((y1, x1), (y2, x2)) = poss
    pr.draw_line(x1*cell_size + int(cell_size/2), y1*cell_size + int(cell_size/2), x2 *
                 cell_size + int(cell_size/2), y2*cell_size + int(cell_size/2), pr.color_alpha(color, 0.7))


def draw_antinode(pos, color):
    (y, x) = pos
    pr.draw_circle_gradient(int((x+0.5)*cell_size), int((y+0.5)*cell_size),
                            cell_size/2, pr.color_alpha(color, 0.8), pr.color_alpha(color, 0.1))


# Initialize the window
grid_len = max(mat.keys())[0] + 1
font_size = 20
cell_size = 26
width = height = grid_len * cell_size
pr.init_window(width, height, "Resonant Collinearity")

pr.set_target_fps(15)
pr.clear_background(pr.BLACK)
time.sleep(4)

for (i, (color, (freq, freq_steps))) in enumerate(zip(colors, steps)):
    pr.clear_background(pr.BLACK)

    # Draw all earlier antinodes
    for (color_in, (_, freq_steps_in)) in list(zip(colors, steps))[:i]:
        for (_, antinodes) in freq_steps_in:
            for poss in antinodes:
                for pos in poss:
                    draw_antinode(pos, color_in)

    # Draw all antennas in their colors
    for ((y, x), freq, color_antenna) in antennas:
        pr.draw_text(freq, x*cell_size + 8, y*cell_size +
                     4, font_size, color_antenna)

    freq_frame = 0

    changes = True
    while changes:
        changes = False

        # Draw a new line
        if freq_frame < len(freq_steps):
            changes = True
            draw_line(freq_steps[freq_frame][0], color)

        # Draw new antinodes
        for (pi, (_, antinodes)) in enumerate(freq_steps[:freq_frame]):
            draw_ind = freq_frame - pi - 1
            if draw_ind < len(antinodes):
                for antinode in antinodes[draw_ind]:
                    changes = True
                    draw_antinode(antinode, color)

        pr.end_drawing()
        freq_frame += 1

# The final end-screen
pr.clear_background(pr.BLACK)

# Draw all earlier antinodes
for (color_in, (_, freq_steps_in)) in list(zip(colors, steps)):
    for (_, antinodes) in freq_steps_in:
        for poss in antinodes:
            for pos in poss:
                draw_antinode(pos, color_in)

# Draw all antennas in their colors
for ((y, x), freq, color_antenna) in antennas:
    pr.draw_text(freq, x*cell_size + 8, y*cell_size +
                 4, font_size, color_antenna)

time.sleep(10)
pr.close_window()
