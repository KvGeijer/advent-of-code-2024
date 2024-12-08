import pyray as pr
import time

with open("input.txt", 'r') as f:
    lines = f.readlines()


# Returns all intermediate strings tried
def valid(ints, target):
    tries = []
    return (valid_rec(ints[0], str(ints[0]), ints[1:], target, tries), target, tries, "   ".join(map(str, ints)))


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
for (target, ints) in sorted(input, reverse=True, key=lambda t: len(t[1]))[:30]:
    processes.append(valid(ints, target))


# Visualize the frames
font_size = 16
char_width = font_size
line_height = 2 + font_size

# Initialize the window
width = char_width*33
height = line_height*len(processes)
pr.init_window(width, height, "Bridge Repair")

# Set target FPS
pr.set_target_fps(100)


# The length to allocate for the target string
target_space = int(char_width*0.6)*max([len(str(target))
                                        for (_, target, _, _) in processes])


errors = ([abs(target - acc) for (_, target, tries, _)
           in processes for (acc, _) in tries])
errors.sort()
mean_off = errors[int(len(errors)*3/4)]


def get_color(diff):
    if diff == "max":
        ratio = 1
    elif diff == 0:
        ratio = 0
    else:
        ratio = (diff / mean_off)**0.1
        ratio = min(1, ratio)
        ratio = max(0.2, ratio)

    red = int(ratio * 255)
    green = int((1 - ratio) * 255)
    return pr.Color(red, green, 0, 255)  # RGB color


frame = 0
done = False
while not done:
    pr.clear_background(pr.BLACK)

    done = True
    for (pi, (valid, target, tries, start_str)) in enumerate(processes):
        # Draw each frame as "target [<>=] tried_string" where I want to use a colormap depending on how close it is
        state_ind = frame - pi*20 - 1
        text_y = pi*line_height
        target_x = 0
        operator_x = target_space + char_width
        acc_x = operator_x + char_width*2
        acc_res_x = acc_x * 2

        pr.draw_text(str(target), target_x, text_y, font_size, pr.WHITE)
        if state_ind >= len(tries) - 1:
            # Print the final state
            if valid:
                # Show it in green, and that it equals
                color = get_color(0)
                pr.draw_text('=', operator_x, text_y, font_size, color)
            else:
                # Show it in red, and that it does not equal
                color = get_color("max")
                # op = '<' if target < tries[-1][0] else '>'
                op = '!='
                pr.draw_text(op, operator_x - 2, text_y, font_size, color)
            pr.draw_text(tries[-1][1], acc_x, text_y, font_size, color)
        elif state_ind >= 0:
            done = False
            # Show a normal intermediate state
            (acc, acc_str) = tries[state_ind]
            color = get_color(abs(acc - target))
            op = '<' if target < acc else '>'
            pr.draw_text(op, operator_x, text_y, font_size, color)
            pr.draw_text(acc_str, acc_x, text_y, font_size, color)
        else:
            done = False
            # Just show the starting string in white, and the target
            color = pr.WHITE
            op = '?'
            pr.draw_text(op, operator_x, text_y, font_size, color)
            pr.draw_text(start_str, acc_x, text_y, font_size, color)

    pr.end_drawing()
    if frame == 0:
        time.sleep(4)
    frame += 1

print("DONE")
time.sleep(10)
pr.close_window()
