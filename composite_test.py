from manim import *

from irving import *
from table import PreferenceTable
from sr_instance import generate_sr_instance

class IrvingScene(Scene):
    def construct(self, preferences=unsat_preferences):
        if not preferences:
            preferences = generate_sr_instance(['a', 'b', 'c', 'd', 'e', 'f'])
        T = PreferenceTable(preferences, scale=1, center=(0,-2))
        G = PreferenceGraph(preferences, scale=1, center=(0,2))
        S = IrvingSolver(preferences=preferences, T=T, G=G, scene=self)
        self.play(*T.create())
        S.match_roommates()