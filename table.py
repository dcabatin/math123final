from manim import *

class PetarMatrix(MobjectMatrix):
    """Matrix with no brackets"""
    def add_brackets(self, left="\\big[", right="\\big]"):
        pass


class PreferenceTable():

    def __init__(self, prefs, center=None, scale=None):
        self.prefs = prefs
        self.center = center
        self.scale = scale

        self.order = sorted(prefs.keys())
        self.key_mobs = {k : Text(k) for k in self.order}
        self.pref_mobs = {
            player : {
                k : Text(k) for k in self.prefs[player]
            }
            for player in self.order
        }
        
        self.mob_matrix = np.zeros((len(prefs), len(prefs)), dtype=object)

        for i, player in enumerate(self.order):
            self.mob_matrix[i][0] = self.key_mobs[player]
            for j, pref in enumerate(self.prefs[player]):
                self.mob_matrix[i][j+1] = self.pref_mobs[player][pref]

        self.matrix_mob = PetarMatrix(
            self.mob_matrix,
            left_bracket="|",
            right_bracket="|"
        )

        self.lines = self.get_lines()
        
        

        
    def get_lines(self):

        lines = []

        left_x = self.matrix_mob.get_left()[0]
        right_x = self.matrix_mob.get_right()[0]

        for i in range(len(self.mob_matrix)-1):
            prev_row = self.mob_matrix[i][0].get_bottom()
            next_row = self.mob_matrix[i+1][0].get_top()

            y = (prev_row[1] + next_row[1]) / 2
            
            start = (left_x, y, 0)
            end = (right_x, y, 0)

            lines.append(Line(start, end))
        
        top_y = self.matrix_mob.get_top()[1]
        bot_y = self.matrix_mob.get_bottom()[1]

        m1 = self.matrix_mob[0][0]
        m2 = self.matrix_mob[0][1]
        vbar_x = (m1.get_right()[0] + m2.get_left()[0])/2

        lines.append(
            Line((vbar_x, top_y, 0), (vbar_x, bot_y, 0))
        )

        return lines

    def create(self):
        matrix_anim = ShowCreation(self.matrix_mob)
        line_anims = [ShowCreation(l) for l in self.lines]
        return [matrix_anim]+line_anims