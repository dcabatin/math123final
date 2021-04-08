from manim import *

from table import PreferenceTable

class TestTable(Scene):
    def construct(self):
        a = "A"
        b = "B"
        c = "C"
        d = "D"
        preferences = {
            a : [b, c, d],
            b : [c, d, a],
            c : [a, b, d],
            d : [a, b, c]
        }
        t = PreferenceTable(preferences)
        self.play(*t.create())
        self.play(t.propose(b, d))
        self.play(*t.accept_proposal(b, d), run_time=0.3)
        self.play(*t.reject_proposal(b, d))
        self.play(*t.reject_proposal(a, b))
        self.play(*t.uncreate())
        self.wait()
