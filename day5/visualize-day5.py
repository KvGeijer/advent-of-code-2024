from manim import MovingCameraScene, VGroup, Text, UpdateFromFunc, AnimationGroup, LaggedStart
from manim import GRAY, LEFT, RIGHT, DOWN, UP, GREEN, RED
from collections import defaultdict


class ReportVisualization(MovingCameraScene):
    def construct(self):
        # Generate sample reports
        with open("input.txt") as f:
            rules_txt, reports_txt = f.read().strip().split("\n\n")

        deps = defaultdict(list)
        for pre, post in map(lambda x: x.split("|"), rules_txt.split("\n")):
            deps[int(post)].append(int(pre))

        reports = [[int(c) for c in line.split(",")]
                   for line in reports_txt.split("\n")]

        def isvalid(update):
            use = set(update)
            done = set()
            for item in update:
                for dep in use & set(deps[item]):
                    if dep not in done:
                        return False
                done.add(item)
            return True

        def repair(update):
            use = set(update)
            done = []
            while len(done) < len(update):
                for item in update:
                    if item not in done:
                        if all(d in done for d in set(deps[item]) & use):
                            done.append(item)
            return done

        def score(report):
            return report[len(report)//2]

        duration = 20  # Total duration of the animation
        report_spacing = 0.3  # Spacing between reports (adjust as needed)

        # Initialize sums
        sum_valid = 0
        sum_invalid = 0

        # Display positions
        report_texts = []
        for i, report in enumerate(reports):
            # Create a VGroup for each report consisting of Text objects for each integer
            numbers = VGroup()
            for j, num in enumerate(report):
                num_text = Text(str(num), color=GRAY, font_size=18)
                if j == 0:
                    # Position the first number of the report
                    y_position = 3.4 - i * report_spacing
                    num_text.move_to(UP * y_position)
                    num_text.to_edge(LEFT, buff=0.2)
                else:
                    # Position subsequent numbers to the right of the previous one
                    num_text.next_to(numbers[-1], RIGHT, buff=0.2)
                numbers.add(num_text)
            report_texts.append(numbers)

        # Group all reports together
        all_reports = VGroup(*report_texts)
        self.add(all_reports)

        # Display the sums on the right
        sum_valid_text = Text(f"Part 1: {sum_valid}", color=GREEN)
        sum_invalid_text = Text(f"Part 2: {sum_invalid}", color=RED)

        # Position sum texts
        sum_valid_text.to_corner(UP + RIGHT)
        sum_invalid_text.next_to(sum_valid_text, DOWN)
        self.add(sum_valid_text, sum_invalid_text)

        # List to hold all animations
        all_animations = []

        # Process each report
        for i, report in enumerate(reports):
            report_text = report_texts[i]

            if isvalid(report):
                # Update the valid sum
                score_value = score(report)
                sum_valid += score_value

                # Function to update the valid sum display
                def update_sum_valid(text, sum_valid=sum_valid):
                    new = Text(f"Part 1: {sum_valid}",
                               color=GREEN).move_to(self.camera.frame.get_corner(UP + RIGHT) + 2.9*LEFT + 0.6*DOWN)
                    text.become(new)

                # Animations for a valid report
                anims = [
                    report_text.animate.set_color(GREEN),
                    UpdateFromFunc(sum_valid_text, update_sum_valid)
                ]
                anim_group = AnimationGroup(*anims)
                all_animations.append(anim_group)
            else:
                # Repair the invalid report
                repaired_report = repair(report)
                score_value = score(repaired_report)
                sum_invalid += score_value

                # Animations for moving and recoloring numbers
                animations_movement = []
                # Map numbers to their occurrences to handle duplicates
                num_to_indices = {}
                for index, num in enumerate(report):
                    num_to_indices.setdefault(num, []).append(index)
                repaired_num_to_indices = {}
                for index, num in enumerate(repaired_report):
                    repaired_num_to_indices.setdefault(num, []).append(index)

                # Animate each number moving to its new position and changing color
                for num in report:
                    orig_index = num_to_indices[num].pop(0)
                    new_index = repaired_num_to_indices[num].pop(0)
                    start_num = report_text[orig_index]
                    end_pos = report_text[new_index].get_center()
                    anim = start_num.animate.move_to(end_pos).set_color(RED)
                    animations_movement.append(anim)

                # Function to update the invalid sum display
                def update_sum_invalid(text, sum_invalid=sum_invalid):
                    new = Text(f"Part 2: {sum_invalid}",
                               color=RED).next_to(sum_valid_text, DOWN)
                    text.become(new)
                    # text.next_to(sum_valid_text, DOWN).shift(
                    #     self.camera.frame.get_center() - ORIGIN)

                anims = [
                    AnimationGroup(*animations_movement),
                    UpdateFromFunc(sum_invalid_text, update_sum_invalid)
                ]
                anim_group = AnimationGroup(*anims)
                all_animations.append(anim_group)

        # Calculate total camera shift
        camera_shift_amount = (
            len(reports) - 26) * report_spacing

        # Animate the camera moving upwards
        camera_movement = self.camera.frame.animate.shift(
            DOWN * camera_shift_amount)

        # Play all animations with overlaps using LaggedStart
        # duration = 30  # Total duration of the animation
        self.play(
            LaggedStart(*all_animations, lag_ratio=duration *
                        0.95/len(reports)),
            camera_movement,
            run_time=duration
        )
        self.wait(2)
