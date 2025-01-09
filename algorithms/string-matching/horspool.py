"""
Animation of Horspool's algorithm for string matching. 
"""
from manim import *
import numpy as np

FONT_FAMILY = "Monospace"
ALL_CHARS = " ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class Horspool(Scene):
    """
    Runs Horspool's string matching algorithm 
    to search text for pattern. 
    Returns the start index of the first occurrence of pattern in text, 
    or -1 if pattern never appears. 
    """
    def construct(self):
        # text = "BARD LOVED BANANAS"
        # pattern = "BAN"
        text = "BAAAABAAABAAAAAAAAAABAAAAAABAAAA"
        pattern = "BAAAAAA"

        def compute_shift_table(pattern=pattern):
            """
            Compute the Horspool shift table for all capital letters
            from A to Z, but starting with the blank space character, 
            for the given pattern. 
            """
            shift_table = np.zeros(len(ALL_CHARS), dtype=int)
            for i, char in enumerate(ALL_CHARS):
                # set shift table amount for char
                if char in pattern:
                    try: 
                        shift_table[i] = len(pattern) - 1 - pattern[:-1].rindex(char)
                    except ValueError: 
                        # Occurs when char only appears in pattern as the last character
                        shift_table[i] = len(pattern) - 1
                else:
                    shift_table[i] = len(pattern)
            
            return shift_table
    
        def run_horspool(text=text, pattern=pattern):
            """
            Run Horspool's algorithm and return a 
            summary of the algorithms behavior as a tuple of 
            start indices, i values, and answer values.
            """
            pattern_length = len(pattern)
            start = 0
            shift_table = compute_shift_table(pattern)
            i = pattern_length - 1

            start_indices = []
            i_values = []
            answer_values = []

            while start + pattern_length < len(text):
                i = pattern_length - 1
                start_indices.append(start)
                i_values.append(i)
                answer_values.append("?")

                progress = 0
                while i >= 0 and pattern[i] == text[start + i]:
                    i -= 1
                    progress += 1
                    start_indices.append(start)
                    i_values.append(i)
                    answer_values.append("?")
                if i == -1:
                    answer_values[-1] = start
                    return [start_indices, i_values, answer_values]
                else:
                    print("MISMATCH: ", text[start + i], " != ", pattern[i])
                    print("SHIFT FOR ", text[start + i], " = ", shift_table[ALL_CHARS.index(text[start + i])]) 
                    start += shift_table[ALL_CHARS.index(text[start + i])] - progress
                    
            
            start_indices.append(start)
            i_values.append(i)
            answer_values.append(-1)
            return [start_indices, i_values, answer_values]


        start_indices, i_values, answer_values = run_horspool(text, pattern)
        # print(len(start_indices), len(i_values), len(answer_values))
        
        info_font_size = 24
        start_mob = Text(f"start = {start_indices[0]}", font=FONT_FAMILY, font_size=info_font_size)
        i_mob = Text(f"i = {i_values[0]}", font=FONT_FAMILY, font_size=info_font_size)
        answer_mob = Text(f"result = {answer_values[0]}", font=FONT_FAMILY, font_size=info_font_size)
        
        info_groups = [VGroup(start_mob, i_mob, answer_mob)]

        for start, i, answer in zip(start_indices, i_values, answer_values):
            start_mob_transformed = Text(f"start = {start}", font=FONT_FAMILY, font_size=info_font_size)
            i_mob_transformed = Text(f"i = {i}", font=FONT_FAMILY, font_size=info_font_size)
            answer_mob_transformed = Text(f"result = {answer}", font=FONT_FAMILY, font_size=info_font_size)
            info_groups.append(VGroup(start_mob_transformed, i_mob_transformed, answer_mob_transformed))
        
        # print(len(info_groups))

        for info_group in info_groups:
            info_group.arrange(DOWN, center=False, aligned_edge=LEFT)
            info_group.to_corner(UL)
            # self.play(Write(info_group))
            # self.wait(1)

        text_mob = Text(text, font=FONT_FAMILY, t2c={pattern: YELLOW})
        # Add pattern_mob left-aligned below text_mob
        pattern_mob = Text(pattern, font=FONT_FAMILY).next_to(text_mob, DOWN, aligned_edge=LEFT)
        pattern_mob_pos = pattern_mob.get_left()
        CHAR_WIDTH = text_mob.get_width() / len(text) # or, text_mob[0].width
        # text_group.arrange(DOWN, center=False, aligned_edge=LEFT)
        self.play(Write(text_mob))
        self.play(Write(pattern_mob))

        self.play(Write(info_groups[0]))
        
        for index in range(1, len(info_groups)):
            self.remove(info_groups[index-1])
            self.add(info_groups[index])
            pattern_mob.next_to(text_mob, DOWN, aligned_edge=LEFT)
            pattern_mob.shift((start_indices[index-1] * CHAR_WIDTH) * RIGHT)
            self.add(pattern_mob)

            self.play(Indicate(text_mob[start_indices[index-1] + i_values[index-1]]))
            self.play(Indicate(pattern_mob[i_values[index-1]]))

            self.wait(0.4 if (index < len(start_indices) 
                              and start_indices[index] == start_indices[index - 1]) 
                          else 0.8)

        self.wait(1)
        self.play(FadeOut(info_groups[-1][1]))
        if answer_values[-1] != -1:
            self.play(text_mob[start_indices[-1]:start_indices[-1] + len(pattern)].animate.set_color(GREEN))
        self.wait(3)


        # # Display start, i, answer as info group
        # info_group = VGroup(start_mob, i_mob, answer_mob)
        # info_group.arrange(DOWN, center=False, aligned_edge=LEFT)
        # info_group.to_corner(UL)
        # self.play(Write(info_group))



            # # Left-align text_mob and pattern_mob
            # self.play(FadeOut(text_group))
            # text_group = VGroup(text_mob, pattern_mob)
            # text_group.arrange(DOWN, center=False, aligned_edge=LEFT)
            # self.play(Write(text_group))

            # # Display start and answer
            # self.play(FadeOut(info_group))
            # start_mob = Text(f"start = {start}", font=FONT_FAMILY)
            # info_group = VGroup(start_mob, answer_mob)
            # info_group.arrange(DOWN, center=False, aligned_edge=LEFT)
            # info_group.to_corner(UL)
            # self.play(Write(info_group))
            
            # Wait before next iteration
        #     self.wait(2)



        # if answer_mob.get_text() == "result = ?":
        #     answer_mob = Text(f"result = -1", font=FONT_FAMILY)

        # self.play(FadeOut(start_mob))

        # # Left-align text_mob and pattern_mob
        # text_group = VGroup(text_mob, pattern_mob)
        # text_group.arrange(DOWN, center=False, aligned_edge=LEFT)
        # self.play(Write(text_group))

        # # Display answer
        # info_group = VGroup(answer_mob)
        # info_group.arrange(DOWN, center=False, aligned_edge=LEFT)
        # info_group.to_corner(UL)
        # self.play(Write(info_group))

        
        # text_mob_copy = text_mob.copy()
        # pattern_mob_copy = pattern_mob.copy()
        # text_mob_copy.shift(2 * DOWN)
        # pattern_mob_copy.shift(2 * DOWN)
        # self.play(Write(text_mob_copy), Write(pattern_mob_copy))
        # self.wait(1)

        # pattern_length = len(pattern)
        # text_length = len(text)
        # pattern_mob_copy.generate_target()
        # pattern_mob_copy.target.shift(2 * RIGHT * pattern_length)
        # self.play(MoveToTarget(pattern_mob_copy))
        # self.wait(1)

        # pattern_shift = 0
        # while pattern_shift <= text_length - pattern_length:
        #     for i in range(pattern_length - 1, -1, -1):
        #         if text[pattern_shift + i] != pattern:
        #             break
        #     if i == -1:
        #         self.play(FadeOut(text_mob_copy), FadeOut(pattern_mob_copy))
        #         self.wait(1)
        #         break
        #     else:
        #         pattern_shift += 1
        #         text_mob_copy.generate_target()
        #         text_mob_copy.target.shift(LEFT)
        #         self.play(MoveToTarget(text_mob_copy))
        #         self.wait(1)
        # self.wait(1)
    