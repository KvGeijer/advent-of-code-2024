import pyray as pr
import time

with open("input.txt") as f:
    input = f.read()

# A list with (start, stop, color) for all colored parts
colors = []

# Events, either changin score or enabled/disabled ("score" or "enable", new score or true/false, index)
events = []


def parse_int(input, i):
    if not input[i].isdigit():
        return (False, None)
    else:
        j = i
        while input[j].isdigit():
            j += 1
        return (int(input[i:j]), j)


def parse_mults(input):
    prod = 0
    do = True
    i = 0
    while i < len(input):
        if input[i:i+4] == "do()":
            do = True
            i += 4
            events.append(("enable", True, i - 2))
            colors.append((i-4, i, "enabled"))
        elif input[i:i+7] == "don't()":
            do = False
            i += 7
            events.append(("enable", False, i - 3))
            colors.append((i-7, i, "disabled"))
        elif (input[i:i+4] == "mul("):
            x, j = parse_int(input, i+4)
            if x is False or input[j] != ',':
                i += 1
                continue
            y, j = parse_int(input, j + 1)
            if y is False or input[j] != ')':
                i += 1
                continue
            if do:
                prod += x * y
                color = "tracked"
            else:
                color = "ignored"
            events.append(("score", prod, (i+j)//2))
            colors.append((i, j+1, color))
            i = j + 1
        else:
            i += 1
    return prod


parse_mults(input)


def get_color_by_name(name):
    if name == "enabled":
        return pr.GREEN
    elif name == "disabled":
        return pr.RED
    elif name == "tracked":
        return pr.GOLD
    elif name == "ignored":
        return pr.DARKPURPLE
    elif name == "back":
        return pr.BLACK
    elif name == "cursor":
        return pr.PINK
    elif name == "normal":
        return pr.WHITE
    else:
        return pr.GRAY


def get_char_colors(colors, input_len):
    out = [get_color_by_name("normal")]*input_len
    for (start, stop, color) in colors:
        for ind in range(start, stop):
            out[ind] = get_color_by_name(color)
    return out


def draw_frames(events, colors):
    # Initialize the window
    height = 1640
    width = 2920
    pr.init_window(width, height, "Mull It Over")

    # Set target FPS
    pr.set_target_fps(300)

    # Get char colors in advance
    char_colors = get_char_colors(colors, len(input))
    colored_chars = list(zip(input, char_colors))

    print(len(colored_chars))
    print(colored_chars[-2])

    # Get result and enabled in avcance
    results = [0]
    enabled = [True]
    events.append((None, None, len(input)*2))
    events = events[::-1]
    for ind in range(1, len(input)):
        used = False
        if events[-1][2] == ind and events[-1][0] == "score":
            results.append(events[-1][1])
            used = True
        else:
            results.append(results[-1])
        if events[-1][2] == ind and events[-1][0] == "enable":
            enabled.append(events[-1][1])
            used = True
        else:
            enabled.append(enabled[-1])

        if used:
            events.pop()

    # Draw the text character by character, getting some info
    default_color = get_color_by_name("default")
    font_size = 20
    char_width = pr.measure_text("A", font_size)
    max_chars_per_line = (width - 10) // char_width

    frame = 0
    while not pr.window_should_close() and frame < len(colored_chars):
        # Handle events
        pr.begin_drawing()
        pr.clear_background(get_color_by_name("back"))

        # Only show every 4th frame, for speed
        if (frame % 4) != 0 and frame < len(colored_chars) - 7:
            frame += 1
            continue

        # Draw the lines
        text_x = 10
        text_y = 10
        line_height = font_size + 2  # Line spacing
        for ind, (char, color) in enumerate(colored_chars):
            if ind >= frame:
                color = default_color

            pr.draw_text(char, text_x, text_y, font_size, color)
            text_x += char_width
            if text_x - 10 == max_chars_per_line*char_width:
                text_x = 10
                text_y += line_height

        # Display the enabled and result variables. A bit hacky
        var_font_size = font_size * 3
        enabled_text = "Enabled: "
        pr.draw_text(enabled_text, int(width*0.3), text_y + 30,
                     var_font_size, get_color_by_name("normal"))
        enabled_offset = pr.measure_text(enabled_text, var_font_size)
        enabled_text = str(enabled[frame])
        enabled_color = get_color_by_name(
            "enabled") if enabled[frame] else get_color_by_name("disabled")
        pr.draw_text(enabled_text, int(width*0.3) + enabled_offset,
                     text_y + 30, var_font_size, enabled_color)

        result_text = "Result: "
        pr.draw_text(result_text, int(width*0.55), text_y + 30,
                     var_font_size, get_color_by_name("normal"))
        result_offset = pr.measure_text(result_text, var_font_size)
        result_text = str(results[frame])
        result_color = get_color_by_name("tracked")
        pr.draw_text(result_text, int(width*0.55) + result_offset, text_y
                     + 30, var_font_size, result_color)

        pr.end_drawing()
        if frame == 0:
            time.sleep(3)  # To give you time to start recording

        # Take a screenshot of the image, to generate the video. Too slow, so use screen recording instead
        # if frame % 4 == 0:
        # nbr = frame//4
        # pr.take_screenshot(f"frames/frame_{nbr:05d}.png")

        # Advance to the next frame
        frame += 1

    # Close window
    time.sleep(5)  # To give you time to stop recording
    pr.close_window()


draw_frames(events, colors)
