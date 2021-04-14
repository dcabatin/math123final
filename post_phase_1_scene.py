from manim import *

import preference_graph

accepted_line_config = {
    "color" : preference_graph.ACCEPTED_COLOR,
    "buff": MED_SMALL_BUFF,
    "stroke_width" : 20
}
            

class RejectImpliesNotMatchedScene(Scene):
    def construct(self):
        text1 = Tex("If $y$ rejects $x$ then $x$ and $y$ " + \
                   "cannot \\\\be matched in a stable matching")
        self.add(text1)
        self.play(Write(text1))
        self.wait(1)
        self.play(ApplyMethod(text1.shift, 3 * UP))
        self.wait(1)

        x = LabeledDot(Tex("x'", color=BLACK)).shift(LEFT * 3.2)
        y = LabeledDot(Tex("y'", color=BLACK)).shift(2 * DOWN + LEFT * 0.8)
        
        let_text = Tex("Let $x'$ and $y'$ be the first rejection " + \
                       "s.t. \\\\ $\exists$ $M$ stable " + \
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
        
        Mxy_line = Line(Mx, My, **accepted_line_config)
        
        self.add(Mx, My, Mz, Mxy_line)
        
        M_label = Tex("M", color=WHITE).shift(2.2 * RIGHT)        
        
        left = LEFT * 1.2
        divider = Line(start = 2.4 * DOWN + left, end = UP * 0.6 + left)
        
        self.play(*[
            ApplyMethod(mobj.shift, LEFT * 3)
            for mobj in [x, y, z, xy_arrow, zy_arrow]
        ] + [
            ApplyMethod(mobj.shift, RIGHT * 3)
            for mobj in [Mx, My, Mz, Mxy_line]
        ] + [
            Create(divider)
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
        self.wait(2)
        bullet_placement = 3 * UP + 5 * LEFT
            
        bullet1 = Tex("(1)", color=WHITE).shift(bullet_placement)
        
        self.play(*[
            Uncreate(m)
            for m in [x, y, z, Mx, My, Mz, Mw, xy_arrow, \
                      zy_arrow, Mxy_line, M_label, Mzw_line, \
                      contradiction_label, divider, let_text]
        ] + [
            Write(bullet1)
        ])
                
        text2 = Tex("If $y$ accepts $x$ then $x$ " + \
                    "cannot do \\\\better than $y$").shift(1.5 * UP)
        bullet2 = Tex("(2)", color=WHITE).shift(bullet_placement + 1.5 * DOWN)
        self.play(Write(text2), Write(bullet2))
        self.wait(1)
        follows_text = Tex("(2) follows from (1) as $x$ has been\\\\"+\
                           "rejected by any $z$ it prefers to $y$,\\\\"+\
                           "so $x$ cannot match with $z$ in any\\\\"+\
                           "stable matching").shift(DOWN)
        self.play(Write(follows_text))
        self.wait(1)

        self.play(Uncreate(follows_text))
        self.wait(1)

        text3 = Tex("If $y$ accepts $x$ then $y$ " + \
                    "cannot do \\\\worse than $x$")
        bullet3 = Tex("(3)", color=WHITE).shift(bullet_placement + 3 * DOWN)
        self.play(Write(text3), Write(bullet3))
        self.wait(1)
        
        texts = [bullet1, text1, bullet2, text2, bullet3, text3]

        self.play(*[
            ApplyMethod(t.shift, UP * 3.1)
            for t in texts
        ])

        self.wait(1)
        
        let2_text = Tex("Let $M$ be a matching where $y$\\\\" + \
                        "does worse than $x$").shift(UP * 1.5)

        self.play(Create(let2_text))

        x = LabeledDot(Tex("x", color=BLACK)).shift(LEFT * 1)
        y = LabeledDot(Tex("y", color=BLACK)).shift(2 * DOWN + RIGHT)
        z = LabeledDot(Tex("z", color=BLACK)).shift(2 * DOWN + 3 * LEFT)
        w = LabeledDot(Tex("w", color=BLACK)).shift(RIGHT * 3)

        xz_line = Line(x, z, **accepted_line_config)
        yw_line = Line(y, w, **accepted_line_config)    

        self.play(*[Create(p) for p in [x, y]])
        self.wait(1)
        self.play(*[Create(m) for m in [w, yw_line]])
        self.wait(1)
        self.play(*[Create(m) for m in [z, xz_line]])
        
        xy_line = DashedLine(x, y, buff = MED_SMALL_BUFF)
        self.wait(1)
        self.play(Create(xy_line))
        self.wait(1)
        self.play(*[
            Uncreate(m)
            for m in [x, y, z, w, xz_line, xy_line, yw_line, let2_text]
        ])

        
        self.play(*[
            ApplyMethod(t.shift, DOWN * 3.1)
            for t in texts
        ])

        self.wait(4)
