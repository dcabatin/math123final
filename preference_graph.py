from manim import *

PROPOSAL_COLOR = 'white'
ACCEPTED_COLOR = GREEN # '#30FF30'
REJECTED_COLOR = '#404040'

SENT = 1
REJECTED = 2
ACCEPTED = 3

proposal_arrow_config = {
    "color" : PROPOSAL_COLOR,
}

def accept_arrow(arrow):
    arrow.set_stroke_width(20)
    arrow.tip.set_width(0.5)
    arrow.set_color(ACCEPTED_COLOR)
    
def reject_arrow(arrow):
    arrow.set_stroke_width(7)
    arrow.tip.set_width(0.25)
    arrow.set_color(REJECTED_COLOR)

class PreferenceGraph:
    
    def __init__(self, preferences, center = (0, 0), scale = 1):
        self.prefs = preferences
        self.vertices = sorted(self.prefs.keys())
        self.graph = None
        self.center = center
        self.scale = scale
        self.vertex_config = {
            "radius" : 0.3,
            "stroke_width" : 0,
            "fill_opacity" : 1.0,
            "color" : '#FFFFFF'
        }
        self.proposals = {
            v : {
                u : None
                for u in self.vertices if not v == u
            }
            for v in self.vertices
        }

    def create(self):
        animations = []
        self.graph = Graph(self.vertices, [], labels = True,
                           layout="circular",
                           vertex_config = self.vertex_config)
        self.graph.move_to((*self.center, 0))
        self.graph.scale(self.scale)
        for i in self.vertices:
            animations.append(Create(self.graph[i]))
        return animations

    def propose(self, sender, receiver):
        assert sender in self.graph.vertices, "proposal sender does not exist"
        assert receiver in self.graph.vertices, \
            "proposal receiver does not exist"
        assert not self.proposals[sender][receiver], "proposal already sent"
        
        self.proposals[sender][receiver] = (SENT,
                                            Arrow(self.graph[sender],
                                                  self.graph[receiver],
                                                  z_index=0,
                                                  **proposal_arrow_config))
        return [Create(self.proposals[sender][receiver][1])]

    def reject_proposal(self, sender, receiver):
        assert self.proposals[sender][receiver][0] in {SENT, ACCEPTED}, \
               "proposal either not sent or already rejected"
        
        arrow = self.proposals[sender][receiver][1]
        arrow.set_z_index(-1)
        new_arrow = arrow.copy()
        reject_arrow(new_arrow)
        self.proposals[sender][receiver] = (REJECTED, arrow)
        return [Transform(arrow, new_arrow)]

    def accept_proposal(self, sender, receiver):
        assert self.proposals[sender][receiver][0] == SENT, \
               "proposal either not sent or already rejected/accepted"
        
        arrow = self.proposals[sender][receiver][1]
        arrow.set_z_index(1)
        new_arrow = arrow.copy()
        accept_arrow(new_arrow)
        self.proposals[sender][receiver] = (ACCEPTED, arrow)
        return [Transform(arrow, new_arrow)]

    def uncreate(self):
        animations = []
        for v in self.graph:
            animations.append(Uncreate(v))
        for v in self.vertices:
            for u in self.vertices:
                if not v == u:
                    proposal = self.proposals[v][u]
                    if proposal:
                        animations.append(Uncreate(proposal[1]))
        return animations

    def uncreate_not_accepted_arrows(self):
        animations = []
        for v in self.vertices:
            for u in self.vertices:
                if not v == u:
                    proposal = self.proposals[v][u]
                    if proposal and proposal[0] != ACCEPTED:
                        animations.append(Uncreate(proposal[1]))
                        self.proposals[v][u] = None
        return animations
        
