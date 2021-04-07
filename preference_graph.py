from manim import *


class PreferenceGraph:
    
    def __init__(self, prefs, center = (0, 0), scale = 1):
        self.prefs = prefs
        self.vertices = sorted(self.prefs.keys())
        self.graph = None
        self.center = center
        self.scale = scale
        self.vertex_config = {
            "radius" : 0.3 * scale,
            "stroke_width" : 0,
            "fill_opacity" : 1.0,
            "color" : '#FFFFFF'
        }
        self.proposals = {
            v : {
                u : None
                for u in vertices if v not = u
            }
            for v in vertices
        }


    def create(self):
        animations = []
        print(self.vertices)
        self.graph = Graph(self.vertices, [], labels = True,
                           layout="circular",
                           vertex_config = self.vertex_config)
        for i in self.vertices:
            animations.append(ShowCreation(self.graph[i]))
        return animations

    def propose(self, sender, receiver, accepted):
        assert(sender in self.graph, "proposal sender does not exist")
        assert(receiver in self.graph, "proposal receiver does not exist")
        return []

    def reject_proposal(self, sender, receiver):
        return []

    def accept_proposal(self, sender, receiver):
        return []

    def uncreate(self):
        return []
