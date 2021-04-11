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
        t = PreferenceTable(preferences, center=[-3.5,0,0])
        c = Cycle([a,b,c,a], [b, c, d, b], center=[3,0,0])

        self.play(*t.create())
        # self.play(*c.create())
        As = [
            t.mob_matrix[0][0],
            t.mob_matrix[1][0],
            t.mob_matrix[2][0],
            t.mob_matrix[1][0],
        ]

        Bs = [
            t.mob_matrix[0][1],
            t.mob_matrix[0][2],
            t.mob_matrix[1][2],
            t.mob_matrix[2][2],
        ]

        for anim in c.create_from_table(As, Bs):
            self.play(anim)
            self.wait(2)

        self.wait(2)

        # self.play(*t.propose(b, d))
        # self.play(*t.accept_proposal(b, d), run_time=0.3)
        # self.play(*t.reject_proposal(b, d))
        # self.play(*t.reject_proposal(a, b))
        # self.play(*t.uncreate())
        # self.wait()
