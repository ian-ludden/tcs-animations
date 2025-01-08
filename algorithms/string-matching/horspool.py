"""
Animation of Horspool's algorithm for string matching. 
"""
from manim import *
import numpy as np

FONT_FAMILY = "Monospace"
ALL_CHARS = " ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class Horspool(Scene):
    def construct(self):
        text = "BARD LOVED BANANAS"
        pattern = "BA"

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
            Runs Horspool's string matching algorithm 
            to search text for pattern. 
            Returns the start index of the first occurrence of pattern in text, 
            or -1 if pattern never appears. 
            """
            shift_table = compute_shift_table(pattern)

            start = 0
            pattern_length = len(pattern)

            while start + pattern_length < len(text):
                i = pattern_length - 1
                while i >= 0 and pattern[i] == text[start + i]:
                    i -= 1
                if i == -1:
                    return start
                else:
                    start += shift_table[ALL_CHARS.index(text[start + pattern_length - 1])]

            return -1
    
        shift_table = compute_shift_table(pattern=pattern)
        run_horspool(text=text, pattern=pattern)


        text_mob = Text(text, font=FONT_FAMILY, t2c={pattern: YELLOW})
        pattern_mob = Text(pattern, font=FONT_FAMILY)

        # Left-align text_mob and pattern_mob
        text_group = Group(text_mob, pattern_mob)
        text_group.arrange(DOWN, center=False, aligned_edge=LEFT)

        self.play(Write(text_mob))
        self.play(Write(pattern_mob))
        self.wait(3)
        self.play(text_mob.animate.set_color_by_t2c({pattern: WHITE}))
        self.wait(1)

        
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
    