from manim import *
from bracketless import BracketlessMatrix


class Cycle():

    def __init__(self, As, Bs, center=None):

        self.As = As
        self.Bs = Bs

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

        if center is not None:
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

        self.all_mobjs = self.arrows + [self.cycle_mat]

    def get_arrow(self, i, j):
        return self.arrows[i*2 + (j-i)]

    def accept(self, i, j):
        arrow = self.get_arrow(i, j)
        return [FadeToColor(arrow, GREEN)]

    def reject(self, i, j):
        arrow = self.get_arrow(i, j)
        return [FadeToColor(arrow, GREY_E)]

    def create_from_table(self, table):
        assert (len(self.As) >= 2), "Cycle too small"

        key_mobs = table.key_mobs
        pref_mobs = table.pref_mobs

        all_anims = []

        for i, ai in enumerate(self.As):
            table_ai = key_mobs[ai]
            cycle_ai = self.A_mobs[i]

            anims = [
                TransformFromCopy(table_ai, cycle_ai),
                Create(self.arrows[2*i])
            ]

            if i < len(self.As)-1:
                table_bip1 = pref_mobs[ai][self.Bs[i+1]]
                cycle_bip1 = self.B_mobs[i+1]
                
                anims += [
                    TransformFromCopy(table_bip1, cycle_bip1),
                    Create(self.arrows[2*i+1]),
                ]
                anims += table.propose(ai, self.Bs[i+1])

                if i == 0:
                    table_bi = pref_mobs[ai][self.Bs[i]]
                    cycle_bi = self.B_mobs[i]

                    anims.append(TransformFromCopy(table_bi, cycle_bi))

            all_anims.append(AnimationGroup(*anims))
        
        return all_anims

    def cut_first_prefs(self, table):
        anims = []
        for i in range(0, len(self.arrows), 2):
            anims.append(FadeToColor(self.arrows[i], GREY_E))
            anims += table.reject_proposal(self.As[i//2], self.Bs[i//2])
        
        anims.extend([
            FadeToColor(self.A_mobs[-1], GREY_E),
            FadeToColor(self.B_mobs[0], GREY_E)
        ])

        return anims

    def accept_second_prefs(self, table):
        anims = []
        for i in range(1, len(self.arrows), 2):
            anims.append(FadeToColor(self.arrows[i], GREEN))
            anims += table.accept_proposal(self.As[(i-1)//2], self.Bs[(i+1)//2])
        
        return anims

    def create(self):
        return [Create(m) for m in self.all_mobjs]

    def uncreate(self):
        return [Uncreate(m) for m in self.all_mobjs] 


