from manim import *
from irving import *
from cycle import Cycle
from table import PreferenceTable

class TestCycle(Scene):
    def construct(self):
        

        As = [a, b, c, d]
        Bs = [e, f, g, h]
        C = Cycle(As, Bs)
        T = PreferenceTable()

        self.play(Create(test))
        # self.play(*C.create())

        self.wait()