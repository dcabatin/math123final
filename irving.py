from itertools import combinations
from copy import deepcopy
from cycle import Cycle
from preferences import *
from manim import *
from preference_graph import PreferenceGraph

def validate_preferences(prefs):
    players = sorted(prefs.keys())
    for p, pref in prefs.items():
        assert len(pref) >= len(players) - 1, "Player " + str(p) + " has an incomplete preference list!"
        assert len(pref) <= len(players) - 1, "Player " + str(p) + " has too long of a preference list!"
        assert set(players) - {p} == set(pref), "Player " + str(p) + " should only have other players on their list!"

def validate_incomplete_preferences(prefs):
    players = set(sorted(prefs.keys()))
    for p, pref in prefs.items():
        for q in pref:
            assert q in players, "Player " + str(p) + " has non-player " + str(q) + " in their preference list!" 

class NoStableMatchingException(Exception):
    def __init__(self, msg):
        self.msg = msg

class IrvingSolver():
    def __init__(self, preferences=char_test_preferences, G=None, T=None, scene=None, verbose=False):
        validate_preferences(preferences)
        self.players = sorted(preferences.keys())
        self.n = len(self.players)
        self.preferences = preferences
        self.original_preferences = deepcopy(preferences)
        self.adjacent = self.build_adjacency_matrix()
        self.prune_preferences()
        self.rank = self.build_ranking_matrix()
        self.G = G
        self.T = T
        self.scene = scene
        self.verbose = verbose

    def verify_solution(self, last):
        for p,q in combinations(self.players, 2):
            p_match = self.preferences[p][last[p]]
            p_curr_idx = self.rank[p][p_match]
            p_potential_idx = self.rank[p][q]
            q_match = self.preferences[q][last[q]]
            q_curr_idx = self.rank[q][q_match]
            q_potential_idx = self.rank[q][p]
            if p_curr_idx > p_potential_idx and q_curr_idx > q_potential_idx:
                raise NoStableMatchingException("Failed to verify.")

    def check_unsolvable(self, first=None, last=None):
        for prefs in self.preferences.values():
            if all(pref is None for pref in prefs):
                raise NoStableMatchingException("Stable matching does not exist.")
        if first and last:
            for p in self.players:
                if first[p] > last[p] or first[p] >= len(self.preferences[p]):
                    raise NoStableMatchingException("Stable matching does not exist.")

    def build_ranking_matrix(self):
        rank = {p : { q: len(self.preferences[p]) for q in self.players} for p in self.players}
        for p in self.players:
            for i in range(len(self.preferences[p])):
                q = self.preferences[p][i]
                if q is not None:
                    rank[p][q] = i
        
        return rank

    def build_adjacency_matrix(self):
        return {p: {q: q in self.preferences[p] and p in self.preferences[q] for q in self.players} for p in self.players}

    def prune_preferences(self):
        for p in self.players:
            for i, q in enumerate(self.preferences[p]):
                if not self.adjacent[p][q]:
                    self.preferences[p][i] = None

    def match_roommates(self):
        try:
            first, proposals = self.stable_roommates_phase_1()
            self.between_phases(proposals)

            last = {p: len(self.preferences[p]) - 1 for p in self.players}
            for p in self.players:
                while self.preferences[p][last[p]] is None:
                    last[p] -= 1

            if self.G:
                self.scene.play(*self.G.shift_out())
                self.G = None
                self.scene.wait(3)
          
            self.stable_roommates_phase_2(first, last)
            self.clean_preferences(first, last)
            self.verify_solution(last)

            matches = []
            visited = set()
            i = 0

            for p in self.players:
                if not p in visited:
                    pair = (p, self.preferences[p][last[p]])
                    visited.add(self.preferences[p][last[p]])
                    matches.append(pair)

            if self.scene:
                g = PreferenceGraph(self.original_preferences, center=(3.5,0))
                a, b, c = g.create_from_matching(matches)
                self.scene.play(*a, run_time=1e-6)
                self.scene.play(*b, run_time=1e-6)
                self.scene.play(*c)
                # self.play(*g.uncreate())
                self.scene.wait(4)

            return matches

        except NoStableMatchingException as e:
            if self.verbose:
                print(e.msg)

            return None

    def get_nth_favorite(self, p, n):
        prefs = [q for q in self.preferences[p] if q is not None]
        if n > 0 and len(prefs) <= n:
            return None
        return prefs[n]
    
    def second(self, p):
        return self.get_nth_favorite(p,1)

    def play_animation(self, action, *args, play=True, **kwargs):
        anims = []
        if self.G:
            anims += getattr(self.G, action)(*args, **kwargs)
        if self.T:
            anims += getattr(self.T, action)(*args, **kwargs)
        if not play:
            return anims
        if self.scene:
            self.scene.play(*anims)
            self.scene.wait(0.4)

    def propose(self, p, q, play=True, **kwargs):
        return self.play_animation("propose", p, q, play=play, **kwargs)
        
    def reject(self, p, q, play=True):
        return self.play_animation("reject_proposal", p, q, play=play)
    
    def accept(self, p, q, play=True):
        return self.play_animation("accept_proposal", p, q, play=play)

    def symmetric_reject(self, p, q, play=True):
        anims = []
        if not self.adjacent[p][q]:
            return
        if self.preferences[p][self.rank[p][q]] is not None:
            self.preferences[p][self.rank[p][q]] = None
            if self.scene and self.T:
                anims += self.T.reject_proposal(p, q)
        if self.preferences[q][self.rank[q][p]] is not None:
            self.preferences[q][self.rank[q][p]] = None
            if self.scene and self.T:
                anims += self.T.reject_proposal(q, p)
        if not play:
            return anims
        if self.scene and anims:
            self.scene.play(*anims)

    def one_way_reject(self, p, q):
        self.play_animation("reject_proposal", p, q)
        self.preferences[p][self.rank[p][q]] = None

    def stable_roommates_phase_1(self):
        accepted_proposal = {p: None for p in self.players}
        first = {p: 0 for p in self.players}
        to_process = list(reversed(self.players))
        
        while to_process:
            self.check_unsolvable()
            p = to_process[-1]

            if first[p] >= len(self.preferences[p]):
                raise NoStableMatchingException("Stable matching does not exist.")
            # determine who p should propose to
            while self.preferences[p][first[p]] is None:
                if first[p] >= len(self.preferences[p]):
                    raise NoStableMatchingException("Stable matching does not exist.")
                first[p] += 1
                
            top_pick = self.preferences[p][first[p]]

            
            # top pick hasn't been proposed to yet, so they accept
            if accepted_proposal[top_pick] is None:
                self.propose(p,top_pick, will_be_accepted = True)
                self.accept(p, top_pick)
                accepted_proposal[top_pick] = p
                match_rank = self.rank[top_pick][p]
                to_process.pop()
                continue
            
            # determine if top pick prefers current match to matching with p
            curr_match_idx = self.rank[top_pick][accepted_proposal[top_pick]]
            potential_match_idx = self.rank[top_pick][p]

            # current matching is preferred, i is rejected
            if curr_match_idx < potential_match_idx:
                self.propose(p,top_pick, will_be_accepted = False)
                self.one_way_reject(p, top_pick)
                first[p] += 1 # start at next spot
                continue # keep p in to_process
            
            # accept accepted_proposal, so old match has to return to their preference list again
            else:
                self.propose(p,top_pick, will_be_accepted = True)
                self.one_way_reject(accepted_proposal[top_pick], top_pick)
                self.accept(p, top_pick)
                to_process.pop()
                # add old match to to_process
                to_process.append(accepted_proposal[top_pick])
                accepted_proposal[top_pick] = p
        
        # done processing, so everyone has gotten a proposal accepted
        if self.scene:
            self.scene.wait(2)
        return first, accepted_proposal

    def between_phases(self, proposals):
        for q in self.players:
            p = proposals[q] # q holds a proposal from p
            if self.scene:
                to_circle = self.T.pref_mobs[q][p]
                circle = Circle(color=WHITE).surround(to_circle, buffer_factor=1)
                self.scene.play(Create(circle))
                self.scene.wait(0.3)

            proposal_idx = self.rank[q][p]
            for r in self.original_preferences[q][proposal_idx+1:]:
                self.symmetric_reject(q, r)

            if self.scene:
                self.scene.play(Uncreate(circle))
                self.scene.wait(0.3)

        if self.scene:
            self.scene.wait(2)
                

    def clean_preferences(self, first, last):
        for p in self.players:
            for j in range(len(self.preferences[p])):
                if j < first[p] or j > last[p]:
                    self.symmetric_reject(p, self.original_preferences[p][j])

    def stable_roommates_phase_2(self, first, last):
        while True:
            self.check_unsolvable(first, last)
            p, q = None, None
            # find first p_0 to get a rotation from
            # preference list of p_0 must contain at least 2 elements
            for p_0 in self.players:
                if last[p_0] - first[p_0] > 0 and self.second(p_0) is not None:
                    p, q = self.find_rotation(0, [p_0], [None], first, last)
                    break
            
            if not p and not q:
                return
            
            # eliminate rotation
            self.eliminate_rotation(p, q, first, last)
            if self.scene:
                self.scene.wait(3)

    def find_rotation(self, i, p, q, first, last):
        second_favorite = self.second(p[i])
        next_p = self.preferences[second_favorite][last[second_favorite]]
        
        if next_p in p:
            # rotation found!
            j = p.index(next_p)
            q[j] = second_favorite
                    
            return p[j:], q[j:]

        q.append(second_favorite)
        p.append(next_p)
        return self.find_rotation(i+1, p, q, first, last)

    def animate_rotation_elimination(self, p, q):
        C = Cycle(p + [p[0]], q + [q[0]], center=[3.5,0,0], width=0.9*config['frame_x_radius'])
        for anim in C.create_from_table(self.T):
            self.scene.play(anim)
            self.scene.wait(1)
            
        self.scene.play(*C.cut_first_prefs(self.T))
        self.scene.wait(1)
        self.scene.play(*C.accept_second_prefs(self.T))
        self.scene.wait(1)
        self.scene.play(*C.uncreate())
        self.scene.wait(1)

    def eliminate_rotation(self, p, q, first, last):
        if self.G:
            propose_anims = []
            reject_anims = []
            accept_anims = []
            for i in range(len(p)):
                reject_anims += self.reject(p[i], q[i], play=False)
                if i > 0:
                    accept_anims += self.accept(p[i-1], q[i], play=False)
                if i == len(p) - 1:
                    propose_anims += self.propose(p[i], q[0], play=False, will_be_accepted = True)
                    accept_anims += self.accept(p[i], q[0], play=False)
                else:
                    propose_anims += self.propose(p[i], q[i+1], play=False, will_be_accepted = True)
            if self.scene:
                self.scene.play(*reject_anims)
                self.scene.play(*propose_anims)
                self.scene.play(*accept_anims)
        if self.scene:
            self.animate_rotation_elimination(p, q)

        for i in range(len(p)):
            # q_i rejects p_i so that p_i proposes to q_i+1, then q_i+1 rejects p_i+1 so that ...
            # q_0 rejects p_0 so that p_0 proposes to q_1, then q_1 rejects p_1 and accepts p_0 so that p_1 proposes to q_2, ...
            self.symmetric_reject(p[i], q[i])                
            
            # all successors of p_i-1 are removed from q_i's list, and q_i is removed from their lists
            for j in range(self.rank[q[i]][p[i-1]]+1, last[q[i]]):
                reject = list(self.rank[q[i]].keys())[list(self.rank[q[i]].values()).index(j)]
                self.symmetric_reject(reject, q[i])
                
            last[q[i]] = self.rank[q[i]][p[i-1]]