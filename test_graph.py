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
        g = PreferenceGraph(preferences, scale = 2)
        self.play(*g.create())
        self.play(*g.propose(a, b))
        self.play(*g.propose(a, c))
        self.play(*g.propose(a, d))
        self.wait(1)
        self.play(*g.accept_proposal(a, b))
        self.play(*g.reject_proposal(a, d))
        self.wait(1)
        self.play(*g.uncreate())
        self.wait(1)
