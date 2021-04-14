from manim import *
from bracketless import BracketlessMatrix


class PreferenceTable():

    def __init__(self, prefs, center=None, scale=None, width=None):
        self.prefs = prefs
        self.center = center
        self.scale = scale

        self.order = sorted(prefs.keys())
        self.key_mobs = {k : Text(str(k)) for k in self.order}
        self.pref_mobs = {
            player : {
                k : Text(str(k)) for k in self.prefs[player]
            }
            for player in self.order
        }
        
        self.mob_matrix = np.zeros((len(prefs), len(prefs)), dtype=object)

        for i, player in enumerate(self.order):
            self.mob_matrix[i][0] = self.key_mobs[player]
            for j, pref in enumerate(self.prefs[player]):
                self.mob_matrix[i][j+1] = self.pref_mobs[player][pref]

        self.matrix_mob = BracketlessMatrix(self.mob_matrix)

        self.proposals = {player : {} for player in self.order}

        self.lines = self.make_lines()

        vgroup = self.get_all_mobjs(group=True)

        if center is not None:
            vgroup.move_to(np.array(center))
        if scale is not None:
            vgroup.scale(scale)
        if width is not None:
            vgroup.scale_to_fit_width(width)


        
    def make_lines(self):

        lines = []

        left_x = self.matrix_mob.get_left()[0]
        right_x = self.matrix_mob.get_right()[0]
        slack = 0.3

        for i in range(len(self.mob_matrix)-1):
            prev_row = self.mob_matrix[i][0].get_bottom()
            next_row = self.mob_matrix[i+1][0].get_top()

            y = (prev_row[1] + next_row[1]) / 2
            
            start = (left_x-slack, y, 0)
            end = (right_x+slack, y, 0)

            lines.append(Line(start, end))
        
        top_y = self.matrix_mob.get_top()[1]
        bot_y = self.matrix_mob.get_bottom()[1]

        m1 = self.matrix_mob[0][0]
        m2 = self.matrix_mob[0][1]
        vbar_x = (m1.get_right()[0] + m2.get_left()[0])/2
        
        lines.append(
            Line((vbar_x, top_y+slack, 0), (vbar_x, bot_y-slack, 0))
        )

        return lines

    def get_all_mobjs(self, group=False):
        mat = [self.matrix_mob]
        lines = self.lines
        circles = sum([list(p.values()) for p in self.proposals.values()], [])
        
        all_mobjs = mat + lines + circles

        return VGroup(*all_mobjs) if group else all_mobjs


    def propose(self, sender, receiver, will_be_accepted = None):
        receiver_mob = self.pref_mobs[sender][receiver]
        circle = Circle(color=WHITE).surround(receiver_mob, buffer_factor=1)
        circle.stroke_width = DEFAULT_STROKE_WIDTH*1.7
        circle = DashedVMobject(circle)
        self.proposals[sender][receiver] = circle
        
        return [Create(circle)]

    def accept_proposal(self, sender, receiver):
        receiver_mob = self.pref_mobs[sender][receiver]
        circle = self.proposals[sender][receiver]
        undashed = Circle(color=GREEN).surround(receiver_mob, buffer_factor=1)
        undashed.stroke_width = DEFAULT_STROKE_WIDTH*1.7
        self.proposals[sender][receiver] = undashed
        return [
            ReplacementTransform(circle, undashed),
            FadeToColor(receiver_mob, GREEN)
        ]
    
    def reject_proposal(self, sender, receiver):
        receiver_mob = self.pref_mobs[sender][receiver]
        
        anims = [FadeToColor(receiver_mob, GREY_E)]

        circle = self.proposals[sender].get(receiver, None)

        if circle:
            anims.append(Uncreate(circle))
        
        return anims


    def create(self):
        matrix_anim = Create(self.matrix_mob)
        line_anims = [Create(l) for l in self.lines]
        return [matrix_anim]+line_anims


    def move_anim(self, target):
        all_mobjs = self.get_all_mobjs(group=True)
        all_mobjs.target = np.array(target)
        return [MoveToTarget(all_mobjs)]

    def circle(self, row, player):
        player = self.pref_mobs[row][player]
        circle = Circle(color=WHITE).surround(player, buffer_factor=1)
        self.proposals[row][player] = circle

        return [Create(circle)]


    def uncircle(self, row, player):
        circle = self.proposals[row][player]

        return [Uncreate(circle)]


    def uncreate(self):
        all_mobjs = self.get_all_mobjs(group=False)

        return [Uncreate(m) for m in all_mobjs]
