from manim import *

from table import PreferenceTable

class TestTable(Scene):
    def construct(self):
        a = "a"
        b = "b"
        c = "c"
        d = "d"
        preferences = {
            a : [b, c, d],
            b : [c, d, a],
            c : [a, b, d],
            d : [a, b, c]
        }
        t = PreferenceTable(preferences)
        self.play(*t.create())
        self.wait(5)
