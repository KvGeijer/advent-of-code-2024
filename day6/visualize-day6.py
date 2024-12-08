from copy import deepcopy
import time
import pyray as pr


def vadd(v1, v2):
    return tuple(x + y for (x, y) in zip(v1, v2))


def vsub(v1, v2):
    return tuple(x - y for (x, y) in zip(v1, v2))


def rot(dir):
    match dir:
        case (0,  1):
            return (1,  0)
        case (1,  0):
            return (0, -1)
        case (0, -1):
            return (-1, 0)
        case (-1, 0):
            return (0,  1)


def parse_dir(dir_str):
    match dir_str:
        case 'v':
            return (1, 0)
        case '>':
            return (0, 1)
        case '^':
            return (-1, 0)
        case '<':
            return (0, -1)


with open("input.txt") as f:
    input = f.read().strip()

str_mat = {(row, col): val for(row, r) in enumerate(
    input.split('\n')) for (col, val) in enumerate(r)}

for (row, col), c in str_mat.items():
    if c not in ['#', '.']:
        start_pos = (row, col)
        start_dir = parse_dir(c)
        break

bool_mat = {k: v != '#' for (k, v) in str_mat.items()}

normal_path = []
visited = set()
pos = start_pos
dir = start_dir
while (pos, dir) not in visited and pos in bool_mat.keys():
    visited.add((pos, dir))
    normal_path.append(pos)

    while not bool_mat.get(vadd(pos, dir), True):
        dir = rot(dir)

    pos = vadd(pos, dir)

# Part 1 solution
print(len(set(normal_path)))

# All the cycles found [(obs_pos, cycle_path)]
found_cycles = {}
done = set()
for obs_pos in normal_path[1:][:1]:
    if obs_pos in done:
        continue
    done.add(obs_pos)

    # What if we inserted an obstacle at this position?
    mat = deepcopy(bool_mat)
    mat[obs_pos] = False

    cycle_path = []
    visited = set()
    pos = start_pos
    dir = start_dir
    cycle_started = False
    while (pos, dir) not in visited and pos in mat.keys():
        visited.add((pos, dir))
        if vadd(pos, dir) == obs_pos:
            cycle_started = True

        while not mat.get(vadd(pos, dir), True):
            dir = rot(dir)
            if vadd(pos, dir) == obs_pos:
                cycle_started = True

        if cycle_started:
            cycle_path.append(pos)

        pos = vadd(pos, dir)

    if pos in mat.keys():
        # Cycle!
        found_cycles[obs_pos] = cycle_path

# Part 2 solution
print(len(found_cycles))


# Now to actually visualize it, the idea is to plot the grid as a square, and

# Initialize the window
grid_len = max(bool_mat.keys())[0] + 1
cell_size = 8
width = height = grid_len * cell_size
pr.init_window(width, height, "Guard Gullivant")

# Set target FPS
pr.set_target_fps(120)

traversed = set()
obstacles = [pos for (pos, b) in bool_mat.items() if not b]

for pos in normal_path:
    if pr.window_should_close():
        break

    # Draw the obstacles
    for (row, col) in obstacles:
        pr.draw_rectangle_rounded(pr.Rectangle(
            col*cell_size + 0.5, row*cell_size + 0.5, cell_size - 1, cell_size - 1), 0.5, 4, pr.RED)

    if pos in found_cycles.keys():
        # Draw the obstacle and the cycle
        pass

    # Draw the normal step
    traversed.add(pos)
    for (row, col) in traversed:
        pr.draw_circle_gradient(
            col*cell_size + cell_size//2, row *
            cell_size + cell_size//2, (cell_size-1)/2,
            pr.Color(0, 0, 255, 255), pr.Color(0, 0, 255, 55))
    pr.end_drawing()

time.sleep(10)
pr.close_window()
