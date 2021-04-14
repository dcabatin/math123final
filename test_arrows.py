from manim import *
from SR_arrow import SRArrow

class TestArrows(Scene):
    def construct(self):

        sra = SRArrow(
            start=[-1,0,0],
            end=[1,0,0],
            stroke_width=10,
            tip_length=0.2
        )

        self.play(Create(sra.proposed))
        self.wait()
        self.play(Transform(sra.proposed, sra.accepted))
        self.wait()
        self.play(Transform(sra.accepted, sra.rejected))
        self.wait()
        self.play(Transform(sra.rejected, sra.proposed))
        self.wait()