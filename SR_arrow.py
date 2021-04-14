from manim import *

PROPOSED = 1
REJECTED = 2
ACCEPTED = 3

class SRArrow():
    def __init__(self, start, end, stroke_width, tip_length, state=PROPOSED):
        self.start = start
        self.end = end
        self.stroke_width = stroke_width
        self.tip_length = tip_length
        self.state = state

        assert state in [PROPOSED, REJECTED, ACCEPTED]

        self.accepted = Arrow(
            start=self.start,
            end=self.end,
            stroke_width=self.stroke_width,
            tip_length=self.tip_length,
            max_stroke_width_to_length_ratio=10000,
            max_tip_length_to_length_ratio=10000,
            color=GREEN
        )

        self.proposed = DashedVMobject(Arrow(
            start=self.start,
            end=self.end,
            stroke_width=self.stroke_width,
            tip_length=self.tip_length,
            max_stroke_width_to_length_ratio=10000,
            max_tep_length_to_length_ratio=10000,
            color=WHITE
        ))

        self.rejected = Arrow(
            start=self.start,
            end=self.end,
            stroke_width=self.stroke_width,
            tip_length=self.tip_length,
            max_stroke_width_to_length_ratio=10000,
            max_tip_length_to_length_ratio=10000,
            color=GREY_E
        )
    
    def curr_arrow(self):
        if self.state == ACCEPTED:
            return self.accepted
        elif self.state == REJECTED:
            return self.rejected
        elif self.state == PROPOSED:
            return self.proposed

    def reject(self):
        curr = self.curr_arrow()
        self.state = REJECTED
        return ReplacementTransform(curr, self.rejected)
    
    def accept(self):
        curr = self.curr_arrow()
        self.state = ACCEPTED
        return ReplacementTransform(curr, self.accepted)

            

    
   