from manim import *
from irving_animator import *
from sr_instance import generate_sr_instance

from preference_graph import PreferenceGraph

class TestGraph(Scene):
    def construct(self):
        verts = ["a", "b", "c", "d", "e", "f"]
        preferences = {v : [] for v in verts}
        g = PreferenceGraph(preferences)
        self.play(*g.create())
        self.play(*g.shift_out())
        self.play(*g.propose("a", "b"))
        self.play(*g.propose("a", "c"))
        self.play(*g.propose("a", "d"))
        self.play(*g.propose("a", "e"))
        self.play(*g.propose("a", "f"))
        self.play(*g.propose("b", "e"))
        self.play(*g.propose("d", "f"))
        self.wait(1)
        self.play(*g.accept_proposal("a", "b"))
        self.play(*g.accept_proposal("a", "c"))
        self.play(*g.accept_proposal("a", "d"))
        self.play(*g.reject_proposal("b", "e"))
        self.play(*g.accept_proposal("d", "f"))
        self.play(*g.propose("f", "d"))
        self.play(*g.accept_proposal("f", "d"))
        self.wait(1)
        self.play(*g.shift_in())
        self.play(*g.uncreate())
        self.wait(2)

class TestGraph2(Scene):
    def construct(self):
        verts = ["a", "b", "c", "d", "e", "f"]
        preferences = {v : [] for v in verts}
        g = PreferenceGraph(preferences)
        a, b, c = g.create_from_matching([
            ["a", "c"], ["d", "e"], ["f", "b"]])
        self.play(*a)
        self.play(*b)
        self.play(*c)
        self.play(*g.uncreate())
        
        
class TestGraphIrving(Scene):
    def construct(self, preferences=None):
        if not preferences:
            preferences = generate_sr_instance(['a', 'b', 'c', 'd', 'e', 'f'])
        g = PreferenceGraph(preferences, scale = 1)
        S = IrvingAnimator(preferences=preferences, G=g, scene=self)
        self.play(*g.create())
        S.match_roommates()
