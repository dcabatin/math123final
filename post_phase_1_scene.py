from manim import *

import preference_graph

class RejectImpliesNotMatchedScene(Scene):
    def construct(self):
        text = Tex("If $y$ rejects $x$ then $x$ and $y$ \\\\" + \
                   "cannot be matched in a stable matching")
        self.add(text)
        self.play(Write(text))
        self.wait(1)
        self.play(ApplyMethod(text.shift, 3 * UP))
        self.wait(1)
        x = LabeledDot(Tex("x'", color=BLACK)).shift(LEFT * 3.2)
        y = LabeledDot(Tex("y'", color=BLACK)).shift(2 * DOWN + LEFT * 0.8)

        let_text = Tex("Let $x'$ and $y'$ be the first rejection " + \
                       "s.t. \\\\ $\exists$ a stable matching $M$ " + \
                       "where they are matched").shift(UP * 1.5)
        self.play(Create(x), Create(y), Write(let_text))
        self.wait(1)
        xy_arrow = Arrow(x, y, **preference_graph.proposal_arrow_config)
        self.play(Create(xy_arrow))

        self.play(Transform(xy_arrow,
                            preference_graph.reject_arrow(xy_arrow.copy())))
        z = LabeledDot(Tex("z", color=BLACK)).shift(RIGHT * 0.8)

        self.wait(1)
        
        zy_arrow = Arrow(z, y, **preference_graph.proposal_arrow_config)
        self.play(Create(z), Create(zy_arrow))
        self.play(Transform(zy_arrow,
                            preference_graph.accept_arrow(zy_arrow.copy())))
        self.wait(1)
        Mx = x.copy()
        My = y.copy()
        Mz = z.copy()

        accepted_line_config = {
            "color" : preference_graph.ACCEPTED_COLOR,
            "buff": MED_SMALL_BUFF,
            "stroke_width" : 20
        }
        
        Mxy_line = Line(Mx, My, **accepted_line_config)
        
        self.add(Mx, My, Mz, Mxy_line)

        M_label = Tex("M", color=WHITE).shift(2.2 * RIGHT)        

        self.play(*[
            ApplyMethod(mobj.shift, LEFT * 3)
            for mobj in [x, y, z, xy_arrow, zy_arrow]
        ] + [
            ApplyMethod(mobj.shift, RIGHT * 3)
            for mobj in [Mx, My, Mz, Mxy_line]
        ] + [
            Create(Line(start = 2.4 * DOWN + left, end = UP * 0.6 + left))
            for left in [LEFT * 1.2]
        ] + [
            Create(M_label)
        ])

        Mw = LabeledDot(Tex("w", color=BLACK)).shift(2 * DOWN + RIGHT * 6.2)
        Mzw_line = Line(Mz, Mw, **accepted_line_config)

        self.wait(1)
        
        self.play(Create(Mw), Create(Mzw_line))
        
        self.wait(1)

        contradiction_label = Tex("Thus $w$ rejected $z$ before $z$ proposed to $y$\\\\ and we have reached a contradiction", color=WHITE).shift(3.2 * DOWN)

        self.play(Create(contradiction_label))

        self.wait(5)

        
        
