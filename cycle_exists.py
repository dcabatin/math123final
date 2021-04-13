from manim import *
from cycle import Cycle


class CycleMustExist(Scene):
    def construct(self):
        text1 = Text("How do we know a preference cycle exists?")

        self.play(Write(text1))
        self.wait(1)
        self.play(ApplyMethod(text1.shift, 3 * UP))
        self.wait(2)

        As = [a1, a2, a3, a4] = ["$a_1$", "$a_2$", "$a_3$", "$a_4$"]
        Bs = [b1, b2, b3, b4] = ["$b_1$", "$b_2$", "$b_3$", "$b_5$"]

        C = Cycle(As, Bs)
        A_mobs = C.A_mobs
        B_mobs = C.B_mobs

        self.play(Create(A_mobs[0]))
        self.play(
            Create(B_mobs[0]),
            Create(B_mobs[1]),
            Create(C.arrows[0]),
            Create(C.arrows[1])
        )
        self.wait(2)

        text2 = Tex("$b_2$ must hold a proposal from someone other than $a_1$").shift(2*DOWN)
        text3 = Tex("That player will prefer $b_2$ the most by construction").next_to(text2 ,DOWN)
        self.play(Write(text2))
        self.wait(3)
        self.play(Write(text3))
        self.wait(2)

        self.play(Create(C.arrows[2]))
        self.play(Create(A_mobs[1]))
        self.play(
            Uncreate(text2),
            Uncreate(text3))
        self.wait(2)

        text3 = Tex("$a_2$ must also hold a proposal from someone").shift(2*DOWN)
        text4 = Tex(
            "If $a_2$ holds a proposal from $b_2$ then").next_to(text3, DOWN)
        text5 = Tex(
            "$b_2$ and $a_2$ would already be matched").next_to(text4, DOWN)
        text6 = Tex(
            "$a_1$ would not be on $b_2$'s preference list").next_to(text4, DOWN)
        text7 = Tex(
            "$b_2$ would not be on $a_1$'s preference list").next_to(text4, DOWN)
        
        self.play(Write(text3))
        self.wait(5)
        self.play(Write(text4))
        self.wait()
        self.play(Write(text5))
        self.wait(3)
        self.play(ReplacementTransform(text5, text6))
        self.wait(3)
        self.play(ReplacementTransform(text6, text7))
        self.wait(5)

        self.play(Create(C.arrows[3]))
        self.play(Create(B_mobs[2]))
        self.wait()



        

