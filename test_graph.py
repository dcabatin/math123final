from manim import *
from irving import *
from sr_instance import generate_sr_instance

from preference_graph import PreferenceGraph

class TestGraph(Scene):
    def construct(self, preferences=None):
        if not preferences:
            preferences = generate_sr_instance(['a', 'b', 'c', 'd', 'e', 'f'])
        g = PreferenceGraph(preferences, scale = 1)
        S = IrvingSolver(preferences=preferences, G=g, scene=self)
        self.play(*g.create())
        S.match_roommates()
