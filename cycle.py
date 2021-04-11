from manim import *
from bracketless import BracketlessMatrix


class Cycle():

    def __init__(self, As, Bs, center=None):

        self.A_mobs = list(map(Tex, As))
        self.B_mobs = list(map(Tex, Bs))

        self.mob_matrix = np.zeros((2, len(As)), dtype=object)

        self.mob_matrix[0] = self.A_mobs
        self.mob_matrix[1] = self.B_mobs
        
        self.cycle_mat = BracketlessMatrix(
            self.mob_matrix,
            v_buff=1.5,
            h_buff=2
        )

        if center:
            self.cycle_mat.move_to(np.array(center))
        
        self.arrows = []
        
        for i, a_i in enumerate(self.A_mobs):
            b_i = self.B_mobs[i]
            start = a_i.get_bottom()
            end = b_i.get_top()

            self.arrows.append(
                Arrow(start, end, color=GREEN).set_stroke_width(5)
            )

            if i < len(As)-1:
                b_ip1 = self.B_mobs[i+1]
                start = a_i.get_corner(DOWN+RIGHT)
                end = b_ip1.get_corner(UP+LEFT)

                self.arrows.append(
                    Arrow(start, end, color=WHITE).set_stroke_width(5)
                )

    def create_from_table(self, As, Bs):
        assert (len(As) >= 2), "Cycle too small"
        
        all_anims = []

        for i in range(len(As)):
            table_ai, table_bi = As[i], Bs[i]
            cycle_ai, cycle_bi = self.A_mobs[i], self.B_mobs[i]

            anims = [
                TransformFromCopy(table_ai, cycle_ai),
                Create(self.arrows[2*i])
            ]

            if i < len(As)-1:
                table_bip1 = Bs[i+1]
                cycle_bip1 = self.B_mobs[i+1]
                
                anims += [
                    TransformFromCopy(table_bip1, cycle_bip1),
                    Create(self.arrows[2*i+1]),
                ]

                if i == 0:
                    anims.append(TransformFromCopy(table_bi, cycle_bi))

            all_anims.append(AnimationGroup(*anims))
        
        return all_anims
    

    def create(self):

        return [Create(a) for a in self.arrows] + [Create(self.cycle_mat)]


