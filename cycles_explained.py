from manim import *
from cycle import Cycle

class CycleDefinition(Scene):
    def construct(self):
        title = Text("Preference Cycles:")
        self.play(Create(title))
        self.wait(1)
        self.play(ApplyMethod(title.shift, 3 * UP))
        self.wait(1)
        definition = Tex("A sequence of players $a_1, a_2, \ldots, a_r$", color=WHITE).scale(0.8).shift(1.9 * UP)
        self.play(Create(definition))
        self.wait(1)
        cycle = Cycle(["$a_1$", "$a_2$", "$a_3$", "$a_4$", "$a_5$", "$a_1$"], ["$b_1$", "$b_2$", "$b_3$", "$b_4$", "$b_5$", "$b_1$"], center=[0,-0.5,0])
        self.play(*[Create(a) for a in cycle.A_mobs[:-1]])
        definition2 = Tex("with first preferences $b_1, b_2, \ldots, b_r$", color=WHITE).scale(0.8).shift(1.4 * UP)
        self.play(Create(definition2))
        self.wait(1)
        self.play(*[Create(b) for b in cycle.B_mobs[:-1]])
        
        first_pref_arrows = [arrow for i,arrow in enumerate(cycle.arrows[:-2]) if i % 2 == 0]
        second_pref_arrows = [arrow for i,arrow in enumerate(cycle.arrows[:-2]) if i % 2 == 1]

        self.play(*[Create(ar.curr_arrow()) for ar in first_pref_arrows])
        self.wait(2)
        definition3 = Tex("where the second favorite of $a_i$ is $b_{i+1},$", color=WHITE).scale(0.8).shift(2.4 * DOWN)
        self.play(Create(definition3))
        self.wait(1)
        self.play(*[Create(ar.curr_arrow()) for ar in second_pref_arrows])
        self.wait(2)
        definition4 = Tex("wrapping around for $a_r$ and $a_1$.", color=WHITE).scale(0.8).shift(2.9 * DOWN)
        self.play(Create(definition4))
        self.play(Create(cycle.A_mobs[-1]), Create(cycle.B_mobs[-1]))
        self.play(Create(cycle.arrows[-2].curr_arrow()), Create(cycle.arrows[-1].curr_arrow()))
        self.wait(5)

        self.play(*[Uncreate(d) for d in (definition, definition2, definition3, definition4)])
        self.wait(1)

        elimination = Tex("We \\emph{eliminate} the cycle by having $b_1$ reject $a_1$.", color=WHITE).scale(0.8).shift(1.5 * UP)
        self.play(Create(elimination))
        self.wait(1)

        self.play(*(cycle.reject(0,0) + cycle.reject(5,5)))
        self.wait(1)

        elimination2 = Tex("Each $b_i$ has $a_i$ as its least favorite, so it rejects", color=WHITE).scale(0.8).shift(2.4 * DOWN)
        self.play(Create(elimination2))
        elimination3 = Tex("$a_i$ to match with $a_{i-1}$.", color=WHITE).scale(0.8).shift(2.9 * DOWN)
        self.play(Create(elimination3))
        self.wait(1)

        for i in range(5):
            self.play(*cycle.reject(i+1,i+1))
            self.play(*cycle.accept(i,i+1))

        self.wait(5)
