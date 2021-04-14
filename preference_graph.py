from manim import *
from SR_arrow import SRArrow

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
#    arrow.tip.set_width(0.5)
    arrow.set_color(ACCEPTED_COLOR)
    arrow = VMobject.scale(arrow, 2)
    arrow.scale(0.5)
    arrow.set_stroke_width(20)
    return arrow
    
def reject_arrow(arrow):
    arrow.set_stroke_width(7)
#    arrow.tip.set_width(0.25)
    arrow.set_color(REJECTED_COLOR)
    arrow = VMobject.scale(arrow, 0.5)
    arrow.scale(2)
    arrow.set_stroke_width(7)
    return arrow

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

    def propose(self, sender, receiver, will_be_accepted = None):
        assert sender in self.graph.vertices, "proposal sender does not exist"
        assert receiver in self.graph.vertices, \
            "proposal receiver does not exist"
        assert not self.proposals[sender][receiver], "proposal already sent"

        if will_be_accepted is not None:
            z_index = 1 if will_be_accepted else -1
        else:
            z_index = 0

        arrow = SRArrow(self.graph[sender],
                        self.graph[receiver],
                        stroke_width = 10,
                        tip_length = 0.3,
                        proposed_z_index = z_index)
                      
            
        # arrow = Arrow(self.graph[sender],
        #               self.graph[receiver],
        #               z_index = z_index,
        #               **proposal_arrow_config)
        # arrow.tip.z_index = z_index
            
        # self.proposals[sender][receiver] = (SENT, arrow)
        # return [Create(self.proposals[sender][receiver][1])]
        self.proposals[sender][receiver] = arrow
        return [self.proposals[sender][receiver].propose()]

    def reject_proposal(self, sender, receiver):
        assert self.proposals[sender][receiver].state in {SENT, ACCEPTED}, \
               "proposal either not sent or already rejected"
        
        # arrow = self.proposals[sender][receiver][1]
        # arrow.set_z_index(-1)
        # new_arrow = arrow.copy()
        # new_arrow = reject_arrow(new_arrow)
        # self.proposals[sender][receiver] = (REJECTED, arrow)
        # return [Transform(arrow, new_arrow)]
        return [self.proposals[sender][receiver].reject()]

    def accept_proposal(self, sender, receiver):
        assert self.proposals[sender][receiver].state == SENT, \
               "proposal either not sent or already rejected/accepted"
        return [self.proposals[sender][receiver].accept()]
        # arrow = self.proposals[sender][receiver][1]
        # if self.proposals[receiver][sender] and \
        #    self.proposals[receiver][sender][0] == ACCEPTED:
        #     # we are in phase 2 and have completed a match
        #     other_arrow = self.proposals[receiver][sender][1]
        #     line = other_arrow.copy()
        #     line_endpoints = Line(self.graph[receiver],
        #                           self.graph[sender],
        #                           buff = other_arrow.buff)
        #     for key in ['max_tip_length_to_length_ratio',
        #                 'max_stroke_width_to_length_ratio',
        #                 'preserve_tip_size_when_scaling',
        #                 'initial_stroke_width',
        #                 'tip']:
        #         del line.__dict__[key]
        #     line.__class__ = Line
        #     line.__dict__['family'] = [Line]
        #     line.__dict__['submobjects'] = []
        #     line.start = line_endpoints.start
        #     line.end = line_endpoints.end
        #     line.points = line_endpoints.points

        #     self.proposals[sender][receiver] = (ACCEPTED, other_arrow)
        #     self.proposals[receiver][sender] = (ACCEPTED, line)

        #     new_arrow = other_arrow.copy()
        #     new_arrow.tip.set_width(0.00001)
            
        #     return [Uncreate(arrow),
        #             Transform(other_arrow, new_arrow),
        #             Create(line)]
        # else:
        #     # normal acceptance
        #     arrow.set_z_index(1)
        #     new_arrow = arrow.copy()
        #     new_arrow = accept_arrow(new_arrow)
        #     self.proposals[sender][receiver] = (ACCEPTED, arrow)
        #     return [Transform(arrow, new_arrow)]

    def uncreate(self):
        animations = []
        for v in self.graph:
            animations.append(Uncreate(v))
        for v in self.vertices:
            for u in self.vertices:
                if not v == u:
                    proposal = self.proposals[v][u]
                    if proposal:
                        animations.append(Uncreate(proposal.curr_arrow()))
        return animations

    # def uncreate_not_accepted_arrows(self):
    #     animations = []
    #     for v in self.vertices:
    #         for u in self.vertices:
    #             if not v == u:
    #                 proposal = self.proposals[v][u]
    #                 if proposal and proposal[0] != ACCEPTED:
    #                     animations.append(Uncreate(proposal[1]))
    #                     self.proposals[v][u] = None
    #     return animations
        
