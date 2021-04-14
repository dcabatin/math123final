from manim import *
from cycle import Cycle


class RemovingScene(Scene):
    def construct(self):
        why_text = Tex("Why we can remove cycles")
        self.play(Write(why_text))

        self.play(ApplyMethod(why_text.shift, UP * 3.5))

        lemma1 = r"""
            \begin{align*} \text{Lemma 1: }&\text{in any stable $M$ 
            in the reduced table,}\\
            &a_i\text{ and }b_i \text{ are matched either}\\
            &\text{for all }i \text{ or for no }i\end{align*}"""
        
        lemma1 = Tex(lemma1).next_to(why_text, DOWN * 2)
        self.play(Write(lemma1))

        def math_list(base, start, end):
            return [
                "$" + base + "_" + str(i) + "$"
                for i in range(start, end)
            ]

        As = math_list("a", 1, 5) + ["$a_1$"]
        Bs = math_list("b", 1, 5) + ["$b_1$"]
        
        c = Cycle(As, Bs, center = DOWN * 1.5)
        self.play(*c.create())
        self.wait(1)

        say_text = Tex("Let $b_3$ reject $a_3$") \
                      .next_to(lemma1, DOWN * 2) \
                      .shift(LEFT * 3)
    
        self.play(Write(say_text))

        next_text = Tex("$a_3$ proposes to $b_4$") \
                      .next_to(lemma1, DOWN * 2)   \
                      .shift(RIGHT * 3)
        self.wait(1)
        
        self.play(*c.reject(2, 2))

        self.wait(1)
        self.play(Write(next_text))
        
        self.play(*c.accept(2, 3))
        self.play(*c.reject(3, 3))
        self.play(*c.accept(3, 4))
        self.play(*(c.reject(4, 4) + c.reject(0, 0)))
        self.play(*c.accept(0, 1))
        self.play(*c.reject(1, 1))
        self.play(*c.accept(1, 2))

        self.play(*(c.uncreate()))
        self.wait(1)

        thus_text = Tex(r"""Thus if any $a_i$ is not matched with its $b_i$\\
                then no $a_i$ can match with its $b_i$""") \
                .next_to(lemma1, DOWN * 6)
        
        self.play(Write(thus_text))

        self.wait(1)            
        
        self.play(*[
            Uncreate(m) for m in
            [thus_text, next_text, say_text]
        ])

        
        
        shift_amt = 15
        
        let_m = Tex(r"""
        Let $M$ be a stable matching where each $a_i$ is matched\\
        with its $b_i$. Let $M'$ be the same matching, but each\\
        $a_i$ is matched with its second choice $b_{i+1}$
        """).next_to(why_text, DOWN * 2).shift(RIGHT * shift_amt)

        self.add(let_m)

        self.play(*[
            ApplyMethod(t.shift, LEFT * shift_amt)
            for t in [lemma1, let_m]
        ])

        lemma2 = Tex("Lemma 2: $M'$ is stable if $M$ is stable") \
                    .next_to(let_m, DOWN * 2)

        self.play(Write(lemma2))        

        self.wait()

        As = ["$a_k$", ""]
        Bs = ["$b_k$", "$b_{k+1}$"]
        
        c = Cycle(As, Bs, center = DOWN * 1.5)

        c.reject(0, 0)
        c.accept(0, 1)

        mobjs = c.get_all_mobjs()
        mobjs.pop(2)

        self.play(*[
            Create(m)
            for m in mobjs
        ])

        b_better_text = Tex(r"Each $b_i$ is better\\ off in $M'$ than $M$") \
                           .shift(LEFT * 4 + DOWN)

        self.play(Write(b_better_text))

        a_happy_text = Tex(r"$a_k$ can only prefer \\"+\
                           r"$b_k$ to its current match\\" +\
                           r"but $b_k$ is happier with\\" +\
                           r"$a_{k-1}$, so $M'$ is\\" +\
                           r"stable here") \
                        .shift(RIGHT * 4 + DOWN * 2)

        self.play(Write(a_happy_text))

        self.play(*[
            Uncreate(m)
            for m in mobjs + [b_better_text, a_happy_text]
        ])

        continue_m = Tex(r"Thus $M$ stable $\Rightarrow$ $M'$ stable,\\" +\
                         r"so if there exists a stable matching, we\\" +\
                         r"can find it by proceeding with $M'$ and\\" +\
                         r"eliminating our cycle") \
                         .shift(DOWN * 1.5)

        self.play(Write(continue_m))
        self.wait(2)
        
        self.play(*[
            ApplyMethod(t.shift, RIGHT * shift_amt)
            for t in [lemma1, let_m]
        ] + [
            Uncreate(m)
            for m in [continue_m]
        ] + [
            ApplyMethod(t.shift, DOWN * 0.8)
            for t in [lemma2]
        ])

        plus = TextMobject("+").shift(UP * 0.5)
        
        impl = TextMobject("$\\Leftarrow$") \
               .rotate_in_place(PI/2).shift(DOWN)
        self.play(Create(impl), Create(plus))
        self.wait(1)

        final = Tex(r"We can always eliminate cycles without\\"\
                    r"changing the result").next_to(impl, DOWN)
        self.play(Write(final))
        self.wait(2)

