from manim import *
from cycle import Cycle

class CycleDefinition(Scene):
    def construct(self):
        title = Text("Preference Cycles:")
        self.play(Create(title))
        self.wait(1)
        self.play(ApplyMethod(title.shift, 3 * UP))
        self.wait(1)
        definition = Tex("A sequence of players $a_1, a_2, \ldots, a_r$", color=WHITE).scale(0.8).shift(2 * UP)
        self.play(Create(definition))
        self.wait(1)
        cycle = Cycle(["$a_1$", "$a_2$", "$a_3$", "$a_4$", "$a_5$", "$a_1$"], ["$b_1$", "$b_2$", "$b_3$", "$b_4$", "$b_5$", "$b_1$"], center=[0,-0.5,0])
        self.play(*[Create(a) for a in cycle.A_mobs[:-1]])
        definition2 = Tex("with first preferences $b_1, b_2, \ldots$", color=WHITE).scale(0.8).shift(1.3 * UP)
        self.play(Create(definition2))
        self.wait(1)
        self.play(*[Create(b) for b in cycle.B_mobs[:-1]])
        
        first_pref_arrows = [arrow for i,arrow in enumerate(cycle.arrows[:-2]) if i % 2 == 0]
        second_pref_arrows = [arrow for i,arrow in enumerate(cycle.arrows[:-2]) if i % 2 == 1]

        self.play(*[Create(ar) for ar in first_pref_arrows])
        self.wait(2)
        definition3 = Tex("Where the second favorite of $a_i$ is $b_{i+1},$", color=WHITE).scale(0.8).shift(2.3 * DOWN)
        self.play(Create(definition3))
        self.wait(1)
        self.play(*[Create(ar) for ar in second_pref_arrows])
        self.wait(2)
        definition4 = Tex("wrapping around for $a_r$ and $a_1$.", color=WHITE).scale(0.8).shift(2.9 * DOWN)
        self.play(Create(definition4))
        self.play(Create(cycle.A_mobs[-1]), Create(cycle.B_mobs[-1]))
        self.play(Create(cycle.arrows[-2]), Create(cycle.arrows[-1]))
        self.wait(5)


class CycleMustExist(Scene):
    def construct(self):
        pass

class RemovingCyclesMaintainsSolution(Scene):
    def construct(self):
        pass