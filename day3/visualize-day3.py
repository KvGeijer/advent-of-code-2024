import pyray as pr
import time

with open("input.txt") as f:
    input = f.read()


# Just use the same pattern as my zote code, but only for part 2
# But now also record states. What do I want to show?
# Show the whole input string, but highlight the character i in each step
# If we match something, highlight it in green or something for two frames?
# Also, show the do and prod variable over time. We now have a reactive state, mostly recording diffs:
# State: (
#            (highlight_cursor: bool, ind),
#            (add_highlight: bool, highlight_color: str, start, stop),
#            enabled: bool,
#            result: int
# )
states = []


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
    states.append(((False, None), (False, None, None, None), do, prod))
    while i < len(input):
        if input[i:i+4] == "do()":
            states.append
            do = True
            states.append(
                ((False, i), (True, "enabled", i, i+4), do, prod))
            i += 4
        elif input[i:i+7] == "don't()":
            do = False
            states.append(
                ((False, i), (True, "disabled", i, i+7), do, prod))
            i += 7
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
                states.append(
                    ((False, i), (True, "tracked", i, j+1), do, prod))
            else:
                states.append(
                    ((False, i), (True, "ignored", i, j+1), do, prod))
            i = j + 1
        else:
            states.append(((True, i), (False, None, None, None), do, prod))
            i += 1
    return prod


print(parse_mults(input))


def get_color_by_name(name):
    if name == "enabled":
        return pr.GREEN
    elif name == "disabled":
        return pr.RED
    elif name == "tracked":
        return pr.GOLD
    elif name == "ignored":
        return pr.GRAY
    elif name == "back":
        return pr.BLACK
    elif name == "cursor":
        return pr.PINK
    elif name == "normal":
        return pr.WHITE
    else:
        return pr.BLACK


def draw_frames():
    # Initialize the window
    height = 1640
    width = 2920
    pr.init_window(width, height, "Mull It Over")

    # Set target FPS
    pr.set_target_fps(120)

    # Initialize permanent highlights
    permanent_highlights = []

    frame = 0
    while not pr.window_should_close() and frame < len(states):
        # Handle events
        pr.begin_drawing()
        pr.clear_background(get_color_by_name("back"))

        # Get the current state
        state = states[frame]
        highlight_cursor, ind = state[0]
        add_highlight, highlight_color, start, stop = state[1]
        enabled = state[2]
        result = state[3]

        # Update permanent highlights
        if add_highlight:
            permanent_highlights.append((highlight_color, start, stop))

        # Only show every 4th frame, for speed
        if (frame % 4) != 0:
            frame += 1
            continue

        # Build the list of colors for characters in window
        window_char_colors = [get_color_by_name("normal")] * len(input)

        # Apply permanent highlights
        for color_name, start_idx, end_idx in permanent_highlights:
            color = get_color_by_name(color_name)
            for i in range(start_idx, end_idx):
                window_char_colors[i] = color

        # Apply cursor highlight
        if highlight_cursor:
            idx_in_window = ind
            window_char_colors[idx_in_window] = get_color_by_name("cursor")

        # Draw the text character by character
        font_size = 20
        char_width = pr.measure_text("A", font_size)
        max_chars_per_line = (width - 10) // char_width  # text_width

        # Build the lines
        lines = []
        current_line = ""
        current_colors = []
        current_line_length = 0
        for i, char in enumerate(input):
            current_line += char
            current_colors.append(window_char_colors[i])
            current_line_length += 1
            if current_line_length >= max_chars_per_line:
                lines.append((current_line, current_colors))
                current_line = ""
                current_colors = []
                current_line_length = 0
        if current_line:
            lines.append((current_line, current_colors))

        # Draw the lines
        text_x = 10
        text_y = 10
        line_height = font_size + 2  # Line spacing
        for line_num, (line_text, line_colors) in enumerate(lines):
            y = text_y + line_num * line_height
            x = text_x

            for j, char in enumerate(line_text):
                color = line_colors[j]
                pr.draw_text(char, x, y, font_size, color)
                x += char_width

        # Display the enabled and result variables. A bit hacky
        var_font_size = font_size * 3
        enabled_text = "Enabled: "
        pr.draw_text(enabled_text, int(width*0.3), text_y + len(lines)
                     * line_height + 20, var_font_size, get_color_by_name("normal"))
        enabled_offset = pr.measure_text(enabled_text, var_font_size)
        enabled_text = str(enabled)
        enabled_color = get_color_by_name(
            "enabled") if enabled else get_color_by_name("disabled")
        pr.draw_text(enabled_text, int(width*0.3) + enabled_offset, text_y + len(lines)
                     * line_height + 20, var_font_size, enabled_color)

        result_text = "Result: "
        pr.draw_text(result_text, int(width*0.55), text_y + len(lines)
                     * line_height + 20, var_font_size, get_color_by_name("normal"))
        result_offset = pr.measure_text(result_text, var_font_size)
        result_text = str(result)
        result_color = get_color_by_name("tracked")
        pr.draw_text(result_text, int(width*0.55) + result_offset, text_y + len(lines)
                     * line_height + 20, var_font_size, result_color)

        pr.end_drawing()
        if frame == 0:
            time.sleep(3)  # To give you time to start recording

        # Take a screenshot of the image, to generate the video
        # if frame % 4 == 0:
        # nbr = frame//4
        # pr.take_screenshot(f"frames/frame_{nbr:05d}.png")

        # Advance to the next frame
        frame += 1

    # Close window
    time.sleep(5)  # To give you time to stop recording
    pr.close_window()


draw_frames()
