import pyray as pr
import random


with open('input.txt') as f:
    mat = {(row, col): c for (row, line) in enumerate(f.read().split("\n"))
           for (col, c) in enumerate(line)}


def vadd(x, y):
    return tuple(xx + yy for (xx, yy) in zip(x, y))


def vmul(x, mul):
    return tuple(xx * mul for xx in x)


def vsub(x, y):
    return tuple(xx - yy for (xx, yy) in zip(x, y))


def rot(point):
    (r, c) = point
    return (c, -r)


def div2(point):
    (r, c) = point
    return (r/2, c/2)


visited = set()


def dfs(pos):
    if pos in visited:
        return []
    visited.add(pos)

    found = [("node", pos)]
    for neigh in (vadd(pos, dir) for dir in random.sample(((0, 1), (0, -1), (1, 0), (-1, 0)), 4)):
        if mat.get(neigh, None) == mat[pos]:
            found.append(("conn", (pos, neigh)))
            found.extend(dfs(neigh))
        else:
            found.append(("edge", (pos, neigh)))
    return found


# We don't do part 2, as I don't see any extra flavor gained from visualizing it
p1 = 0
region_processing = []
for pos in mat.keys():
    if pos in visited:
        continue

    start_len = len(visited)
    process = dfs(pos)
    region_processing.append(process)
    edges = [thing for (type, thing) in process if type == "edge"]
    p1 += (len(visited) - start_len) * len(edges)

print(p1)

# Now start processes staggered, drawing a frame from one at a time.
# Would be very nice to useg something like Manim to make things such as staggered overlapping animations easier
grid_len = max(mat.keys())[0] + 1
cell_size = 9
width = height = grid_len * cell_size + cell_size + cell_size//2
pr.init_window(width, height, "Garden Groups")
pr.set_target_fps(fps := 60)

letters = set(mat.values())
colors = [pr.color_from_hsv(i/len(letters)*360, 0.8, 1)
          for i in range(len(letters))]
colors = dict(zip(letters, colors))
edge_color = pr.color_alpha(pr.WHITE, 0.8)


def draw_cell(pos, color):
    (y, x) = pos
    pr.draw_rectangle((x+1)*cell_size, (y+1)*cell_size,
                      cell_size - 3, cell_size - 3, color)


def draw_conn(edge, color):
    (pos1, pos2) = edge

    start = tuple((x + 1)*cell_size + cell_size//2 - 1 for x in pos1[::-1])
    end = tuple((x + 1)*cell_size + cell_size//2 - 1 for x in pos2[::-1])

    pr.draw_line_ex(start, end, cell_size//2, color)


def draw_edge(edge, color):
    (pos1, pos2) = edge
    dir = vsub(pos1, pos2)
    avg = div2(vadd(pos1, pos2))
    start = vadd(avg, div2(rot(dir)))
    end = vadd(avg, (-i for i in div2(rot(dir))))

    start = tuple((x + 1.5)*cell_size - 1.5 for x in start[::-1])
    end = tuple((x + 1.5)*cell_size - 1.5 for x in end[::-1])

    pr.draw_line_ex(start, end, cell_size//8, color)


def draw_region(process):
    for (type, data) in process:
        if type == 'edge':
            draw_edge(data, edge_color)
        elif type == 'conn':
            draw_conn(data, colors[mat[data[0]]])
        else:
            draw_cell(data, colors[mat[data]])
        yield True

    while True:
        yield False


animations = random.sample([draw_region(process)
                            for process in region_processing], len(region_processing))


# maybe draw the characters here?
pr.clear_background(pr.BLACK)
pr.wait_time(3)

frame = 0
while True:
    pr.begin_drawing()
    frame += 1
    anims = animations[:(frame//2) + 1]
    if not any([next(anim) for anim in anims]):
        if len(anims) < len(animations):
            frame += fps
        else:
            break

    pr.end_drawing()

pr.wait_time(10)
pr.close_window()
