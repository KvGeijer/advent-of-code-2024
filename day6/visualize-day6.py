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
for (oi, obs_pos) in enumerate(normal_path[1:]):
    print(f"{oi}/{len(normal_path)}")
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
        old_dir = dir
        if vadd(pos, dir) == obs_pos:
            cycle_started = True

        while not mat.get(vadd(pos, dir), True):
            dir = rot(dir)
            if vadd(pos, dir) == obs_pos:
                cycle_started = True

        if cycle_started:
            visited.add((pos, old_dir))
            cycle_path.append(pos)

        pos = vadd(pos, dir)

    if pos in mat.keys():
        # Cycle!
        found_cycles[obs_pos] = cycle_path

# Part 2 solution
print(len(found_cycles))


# Now to actually visualize it, the idea is to plot the grid as a square, and

def draw_cycle(cycle, damp):
    in_color = pr.Color(int(24 * damp),
                        int(110 * damp), int(28 * damp), 255)
    out_color = pr.Color(int(24 * damp * 0.5),
                         int(110 * damp * 0.5), int(28 * damp * 0.5), 100)
    for pos in cycle:
        pr.draw_circle_gradient(
            pos[1]*cell_size + cell_size//2, pos[0] *
            cell_size + cell_size//2, (cell_size-1)/2,
            in_color, out_color)


# Initialize the window
grid_len = max(bool_mat.keys())[0] + 1
cell_size = 20
width = height = grid_len * cell_size
pr.init_window(width, height, "Guard Gullivant")

# Set target FPS
pr.set_target_fps(10)

traversed = set()
obstacles = [pos for (pos, b) in bool_mat.items() if not b]

path_ind = 0
rendered_cycles = []
while path_ind < len(normal_path):
    pr.clear_background(pr.BLACK)
    pos = normal_path[path_ind]
    if pr.window_should_close():
        break

    # Draw the obstacles
    for (row, col) in obstacles:
        pr.draw_rectangle_rounded(pr.Rectangle(
            col*cell_size + 1, row*cell_size + 1, cell_size - 2, cell_size - 2), 0.5, 1, pr.Color(125, 6, 6, 255))

    # Draw the normal path
    for (row, col) in traversed:
        pr.draw_circle_gradient(
            col*cell_size + cell_size//2, row *
            cell_size + cell_size//2, (cell_size-1)/2,
            pr.Color(20, 76, 125, 255), pr.Color(15, 44, 69, 0))

    # Draw cycles that are still visible
    for (i, (life, cycle)) in enumerate(rendered_cycles):
        rendered_cycles[i][0] -= 1

        # Now draw the cycle
        damp = (life-0.5)/2
        draw_cycle(cycle, damp)
    rendered_cycles = [arr for arr in rendered_cycles if arr[0] > 0]

    if pos in found_cycles:
        (row, col) = pos
        cycle = found_cycles[pos]
        # Draw the obstacle and the cycle
        pr.draw_ring(pr.Vector2((col+1/2)*cell_size, (row+1/2)*cell_size),
                     cell_size*0.2, (cell_size - 1)/2, 0, 360, 2, pr.Color(222, 62, 18, 255))
        del found_cycles[pos]
        draw_cycle(cycle, 1)
        rendered_cycles.append([2, cycle])
    else:
        # Draw the new step
        traversed.add(pos)
        pr.draw_circle_gradient(
            pos[1]*cell_size + cell_size//2, pos[0] *
            cell_size + cell_size//2, cell_size*0.6,
            pr.Color(7, 137, 250, 255), pr.Color(38, 82, 120, 0))
        path_ind += 1

    pr.end_drawing()
    if path_ind == 1:
        time.sleep(10)


time.sleep(10)
pr.close_window()
