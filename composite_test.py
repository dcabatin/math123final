from manim import *

from irving import *
from table import PreferenceTable
from preference_graph import PreferenceGraph
from sr_instance import generate_sr_instance

class IrvingScene(Scene):
    def construct(self, preferences=unsat_preferences):
        if not preferences:
            preferences = generate_sr_instance(['a', 'b', 'c', 'd', 'e', 'f'])
        T = PreferenceTable(preferences, scale=1, center=[-3.5,0, 0])
        G = PreferenceGraph(preferences, scale=1, center=(4.5,0))
        S = IrvingSolver(preferences=preferences, T=T, G=G, scene=self)
        self.play(*T.create())
        self.play(*G.create())
        S.match_roommates()