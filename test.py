from manim import *

class MovingVertices(Scene):
    def construct(self):
        vertices = [1, 2, 3, 4]
        edges = [(1, 2), (2, 3), (3, 4), (1, 3), (1, 4)]
        g = Graph(vertices, edges, labels=True, layout="circular")
        self.play(ShowCreation(g[1]))
        self.play(ShowCreation(g[2]))
        self.play(ShowCreation(g.edges[(1,2)]))
        self.play(FadeOut(g.edges[(1,2)]))
        self.wait()
        self.play(g[1].animate.move_to([1, 1, 0]),
                  g[2].animate.move_to([-1, 1, 0]),
                  g[3].animate.move_to([1, -1, 0]),
                  g[4].animate.move_to([-1, -1, 0]))
        self.wait()
