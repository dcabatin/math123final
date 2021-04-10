from manim import *

from irving import *
from table import PreferenceTable
from sr_instance import generate_sr_instance

class TestTable(Scene):
    def construct(self, preferences=unsat_preferences):
        if not preferences:
            preferences = generate_sr_instance(['a', 'b', 'c', 'd', 'e', 'f'])
        T = PreferenceTable(preferences, scale = 1)
        S = IrvingSolver(preferences=preferences, T=T, scene=self)
        self.play(*T.create())
        self.play(*T.propose())
        # S.match_roommates()
