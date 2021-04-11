from manim import *
from irving import *
from sr_instance import generate_sr_instance

from preference_graph import PreferenceGraph

class TestGraph(Scene):
    def construct(self):
        verts = ["a", "b", "c", "d", "e", "f"]
        preferences = {v : [] for v in verts}
        g = PreferenceGraph(preferences)
        self.play(*g.create())
        self.play(*g.propose("a", "b"))
        self.play(*g.propose("a", "c"))
        self.play(*g.propose("a", "d"))
        self.play(*g.propose("a", "e"))
        self.play(*g.propose("a", "f"))
        self.play(*g.propose("b", "e"))
        self.wait(1)
        self.play(*g.accept_proposal("a", "b"))
        self.play(*g.accept_proposal("a", "c"))
        self.play(*g.accept_proposal("a", "d"))
        self.play(*g.reject_proposal("b", "e"))
        self.wait(1)
        self.play(*g.uncreate())
        self.wait(1)
    
class TestGraphIrving(Scene):
    def construct(self, preferences=None):
        if not preferences:
            preferences = generate_sr_instance(['a', 'b', 'c', 'd', 'e', 'f'])
        g = PreferenceGraph(preferences, scale = 1)
        S = IrvingSolver(preferences=preferences, G=g, scene=self)
        self.play(*g.create())
        S.match_roommates()
