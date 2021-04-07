from manim import *

from preference_graph import PreferenceGraph

class TestGraph(Scene):
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
        g = PreferenceGraph(preferences)
        self.play(*g.create())
        self.wait(2)
        self.play(*g.propose(a, b, True))
        self.wait(2)
