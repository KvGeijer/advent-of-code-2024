import pyray as pr
import collections
import itertools
import random


mat = {}
with open('input.txt') as f:
    for (row, line) in enumerate(f.readlines()):
        for (col, c) in enumerate(line.strip()):
            mat[(row, col)] = int(c)
ends = [pos for (pos, h) in mat.items() if h == 9]
random.shuffle(ends)


def neighs4(pos):
    (x, y) = pos
    return ((x + 1, y), (x-1, y), (x, y+1), (x, y-1))


def dfs(pos):
    height = mat[pos]
    if height == 0:
        return ((pos,),)
    else:
        return tuple(path + (pos,) for neigh in neighs4(pos) if mat.get(neigh, -1)
                     == height - 1 for path in dfs(neigh))


paths = [path for end in ends for path in dfs(end)]


# Part 2 answer
print(len(paths))

starts = [pos for (pos, h) in mat.items() if h == 0]
random.shuffle(starts)
end_inds = {}
start_inds = {}
for (i, pos) in enumerate(ends):
    end_inds[pos] = i
for (i, pos) in enumerate(starts):
    start_inds[pos] = i

start_paths = {pos: [] for pos in starts}
for path in paths:
    start_paths[path[0]].append(path)


def generate_colors(num_colors):
    # Create a color grid by cycling through R, G, B with steps to distribute colors evenly
    step = int(256 / (num_colors ** (1/3)))
    color_space = range(0, 256, max(1, step))
    rgb_combinations = itertools.product(color_space, repeat=3)
    colors = [pr.Color(r, g, b, 255) for r, g, b in rgb_combinations]
    return colors[:num_colors]


end_colors = generate_colors(len(ends))

# Generate the frames
frames = collections.defaultdict(lambda: [])
for (start_ind, start) in enumerate(starts):
    # Show all paths from a start at once
    for step in range(10):
        for path in start_paths[start]:
            frames[start_ind*4 +
                   step].append((path[step], end_colors[end_inds[path[-1]]]))

# Initialize the window
grid_len = max(mat.keys())[0] + 1
cell_size = 26
width = height = grid_len * cell_size
pr.init_window(width, height, "Hoof It")

fps = 30
pr.set_target_fps(fps)


def draw_cell(pos, color):
    (y, x) = pos
    pr.draw_rectangle(x*cell_size, y*cell_size,
                      cell_size, cell_size, pr.color_alpha(color, 0.2))


def draw_heightmap():
    for (pos, h) in mat.items():
        draw_cell(pos, pr.Color(20*h, 20*h, 20*h, 255))


pr.clear_background(pr.BLACK)
draw_heightmap()
# Delay for 3 seconds, to get time to film (waiting normally clears background)
for delay_frame in range(fps*3):
    pr.end_drawing()

for frame_ind in range(len(frames)):
    for (pos, color) in frames[frame_ind]:
        draw_cell(pos, color)

    pr.end_drawing()

pr.wait_time(10)
pr.close_window()
