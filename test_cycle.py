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
        T = PreferenceTable(preferences, center=[-3.5,0,0])
        C = Cycle([a,b,c,a], [b, c, d, b], center=[3,0,0])

        self.play(*T.create())
        self.play(
            *T.propose(a, b),
            *T.propose(b, c),
            *T.propose(c, d)
        )
        self.play(
            *T.accept_proposal(a, b),
            *T.accept_proposal(b, c),
            *T.accept_proposal(c, d)
        )
        self.wait()
        self.play(*C.create())
        self.play(*C.accept(a, c))
        self.play(*C.reject(a, b))
        self.wait()
        # for anim in C.create_from_table(T):
        #     self.play(anim)
        #     self.wait(2)
        
        # self.play(*C.cut_first_prefs(T))
        # self.wait(2)
        # self.play(*C.accept_second_prefs(T))
        # self.wait(2)
        # self.play(*C.uncreate())

        self.wait(2)