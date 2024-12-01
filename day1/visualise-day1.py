from PIL import Image, ImageDraw, ImageFont
import random
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


def quicksort(arr):
    """Quicksort algorithm that returns a list of intermediate sorted states."""
    steps = [(None, None, arr.copy())]  # Record the initial state
    quicksort_rec(arr, steps, 0, len(arr) - 1)
    return steps


def quicksort_rec(arr, states, start, stop):
    """Recursive quicksort with states recorded."""
    if start >= stop:
        return

    # Partition the array, and get indexes to left and right of index
    left_pivot, right_pivot = partition(arr, start, stop, states)

    # Recursively sort the partitions
    quicksort_rec(arr, states, start, left_pivot)
    quicksort_rec(arr, states, right_pivot, stop)


def partition(arr, start, stop, states):
    """Partition the array around a pivot"""

    # Use a random index as pivot
    pivot = arr[random.randint(start, stop)]

    low = start
    high = stop
    while low < high:
        if arr[low] < pivot:
            low += 1
        elif arr[high] >= pivot:
            high -= 1
        else:
            # Swap!
            arr[low], arr[high] = (arr[high], arr[low])
            states.append((low, high, arr.copy()))

    # Home-cooked thing to avoid inf loop
    while high < len(arr) and arr[high] == pivot:
        high += 1

    return low - 1, high


def draw_bars(steps, width, height, scaling_yf):
    """Draw a bar chart representation of the array using PIL."""
    low, high, array = steps

    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    n = len(array)
    bar_width = width // n
    for i, value in enumerate(array):
        bar_height = scaling_yf(value)
        x0 = i * bar_width
        y0 = height - bar_height
        x1 = x0 + bar_width - 1
        y1 = height
        color = "black" if i != low and i != high else "red"
        draw.rectangle([x0, y0, x1, y1], fill=color)
    return img


def combine_sorts(left_img, right_img):
    combined_width = left_img.width + right_img.width + 2
    lower_height = 200
    combined_height = left_img.height + lower_height

    combined_img = Image.new("RGB", (combined_width, combined_height), "white")

    # Paste the left and right images into the combined image
    combined_img.paste(left_img, (0, 0))  # Paste the left image
    combined_img.paste(right_img, (left_img.width + 2, 0))  # Paste the right image

    # Create a black bar between the images
    draw = ImageDraw.Draw(combined_img)
    draw.rectangle([left_img.width, 0, left_img.width + 1, left_img.height - 1], fill="darkblue")

    return combined_img


def add_count(base_img, value, font_size=120):
    img = base_img.copy()
    draw = ImageDraw.Draw(img)
    text = str(value)

    # Load the font
    try:
        font = ImageFont.truetype("arial.ttf", font_size)  # Arial is common on most systems
    except IOError:
        print("Could not find font")
        font = ImageFont.load_default()  # Fall back to default if Arial is not available

    # Calculate text dimensions using textbbox
    text_bbox = draw.textbbox((0, 0), text, font=font)  # (left, top, right, bottom)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # We want the text to stop at 1100
    x = 1200 - text_width
    y = img.height - text_height - 100

    # Draw the text on the image
    draw.text((x, y), text, fill="black", font=font)

    return img


def color_bars(img, index, left_arr, right_arr, scaling_yf, width, height):
    """Function for coloring bars in the combined image at an index"""
    draw = ImageDraw.Draw(img)
    bar_width = (img.width - 2) // (len(left_arr) + len(right_arr))

    # left
    bar_height = scaling_yf(left_arr[index])
    x0 = index * bar_width
    y0 = height - bar_height
    x1 = x0 + bar_width - 1
    y1 = height
    color = "red"
    draw.rectangle([x0, y0, x1, y1], fill=color)

    # right
    bar_height = scaling_yf(right_arr[index])
    x0 = index * bar_width + 2 + width
    y0 = height - bar_height
    x1 = x0 + bar_width - 1
    y1 = height
    color = "red"
    draw.rectangle([x0, y0, x1, y1], fill=color)


def gen_frames(left_steps, right_steps, diff_steps, output_dir):
    """Generate a series of images representing the sorting process."""

    # Remove old frame data
    import os, shutil
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    
    os.makedirs(output_dir, exist_ok=True)

    lower = min(min(left_steps[0][2]), min(right_steps[0][2]))
    upper = max(max(left_steps[0][2]), max(right_steps[0][2]))
    width = 1000 # Hard coded after input size
    height = 668*2
    scaling_yf = lambda y: int(height*(y-lower + upper/50)/(upper*1.02 - lower))
	
    # First visualize the sorting of the two arrays together.
    sort_iters = max(len(left_steps), len(right_steps))
    for i in range(sort_iters):
        left_step = left_steps[i] if i < len(left_steps) else (None, None, left_steps[-1][2])
        right_step = right_steps[i] if i < len(right_steps) else (None, None, right_steps[-1][2])
        print(f"Sorting: {i}/{sort_iters}")

        left_img = draw_bars(left_step, width, height, scaling_yf)
        right_img = draw_bars(right_step, width, height, scaling_yf)

        img = combine_sorts(left_img, right_img)
        img.save(f"{output_dir}/frame_{i:04d}.png")

    # Do a last image, without any coloring of the bars
    left_img = draw_bars((None, None, left_step[2]), width, height, scaling_yf)
    right_img = draw_bars((None, None, right_step[2]), width, height, scaling_yf)

    base = combine_sorts(left_img, right_img)
    base.save(f"{output_dir}/frame_{sort_iters:04d}.png")

    # Then show the running sum of differences.
    # Would be great to do this visually, but for now just a number
    for (i, value) in enumerate(diff_steps):
        print(f"Nbr: {i}/{len(diff_steps)}")
        img = add_count(base, value)
        if i > 0:
            color_bars(img, i - 1, left_step[2], right_step[2], scaling_yf, width, height)
        img.save(f"{output_dir}/frame_{(i+sort_iters+1):04d}.png")


def gen_video(output_dir, framerate = 120):
    """Generate a video from frames using ffmpeg."""
    name = "historian-hysteria-p1.mp4"
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


def main():
    with open("input.txt", 'r') as file:
        input = ints(file.read())

    # Get sorting steps
    left_steps = quicksort(input[::2])
    right_steps = quicksort(input[1::2])

    prefix = [0]
    for (left, right) in zip(left_steps[-1][2], right_steps[-1][2]):
        prefix.append(prefix[-1] + abs(left - right))

    out_dir = "frames"
    gen_frames(left_steps, right_steps, prefix, out_dir)
    gen_video(out_dir)


if __name__ == "__main__":
    main()

