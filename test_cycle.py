from manim import *
from irving import *
from cycle import Cycle
from table import PreferenceTable

class TestCycle(Scene):
    def construct(self):
        a = "a"
        b = "b"
        c = "c"
        d = "d"
        preferences = {
            a : [b, c, d],
            b : [c, d, a],
            c : [d, b, a],
            d : [a, b, c]
        }
        t = PreferenceTable(preferences, center=[-3.5,0,0])
        c = Cycle([a,b,c,a], [b, c, d, b], center=[3,0,0])

        self.play(*t.create())

        for anim in c.create_from_table(t):
            self.play(anim)
            self.wait(2)
        
        self.play(*c.resolve_cycle())
        self.wait()
        self.play(*c.uncreate())

        self.wait(2)