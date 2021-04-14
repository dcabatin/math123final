from manim import *

from irving import *
from table import PreferenceTable
from sr_instance import generate_sr_instance
from cycle import Cycle

class TestTable(Scene):
    def construct(self, preferences=unsat_preferences):
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

        

        t = PreferenceTable(preferences, center=left_center, width=0.9*config.frame_x_radius)

        self.play(*t.create())
        self.play(*t.propose(b, d))
        self.play(*t.accept_proposal(b, d), run_time=0.3)
        self.play(*t.reject_proposal(b, d))
        self.play(*t.reject_proposal(a, b))
        self.play(*t.uncreate())
        self.wait()
