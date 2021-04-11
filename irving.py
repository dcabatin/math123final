from itertools import combinations
from copy import deepcopy

char_test_preferences = {
    'a': ['c', 'd', 'b', 'f', 'e'], 
    'b': ['f', 'e', 'd', 'a', 'c'], 
    'c': ['b', 'd', 'e', 'a', 'f'], 
    'd': ['e', 'b', 'c', 'f', 'a'], 
    'e': ['c', 'a', 'b', 'd', 'f'], 
    'f': ['e', 'a', 'c', 'd', 'b']}

test_preferences = {
    1: [3, 4, 2, 6, 5], 
    2: [6, 5, 4, 1, 3], 
    3: [2, 4, 5, 1, 6], 
    4: [5, 2, 3, 6, 1], 
    5: [3, 1, 2, 4, 6], 
    6: [5, 1, 3, 4, 2]}

unsat_preferences = {
    1: [2,3,4],
    2: [3,1,4],
    3: [1,2,4],
    4: [1,2,3]
}

class NoStableMatchingException(Exception):
    def __init__(self, msg):
        self.msg = msg

class IrvingSolver():
    def __init__(self, preferences=unsat_preferences, G=None, T=None, scene=None, verbose=False):
        self.players = sorted(preferences.keys())
        self.n = len(self.players)
        self.preferences = preferences
        self.original_preferences = deepcopy(preferences)
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
        rank = {p : { q: None for q in self.preferences[p]} for p in self.players}
        for p in self.players:
            for i in range(len(self.preferences[p])):
                q = self.preferences[p][i]
                rank[p][q] = i
        
        return rank

    def match_roommates(self):
        try:
            first, proposals = self.stable_roommates_phase_1()

            # if self.scene:
            #     self.scene.play(*self.G.uncreate())

            self.between_phases(proposals)

            last = {p: len(self.preferences[p]) - 1 for p in self.players}
            for p in self.players:
                while self.preferences[p][last[p]] is None:
                    last[p] -= 1
                    
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
                animations = self.G.uncreate_not_accepted_arrows()
                if len(animations) > 0:
                    self.scene.play(*animations)
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

    def first(self, p):
        return self.preferences[p].index(self.get_nth_favorite(p, 0))
    
    def last(self, p):
        return self.preferences[p].index(self.get_nth_favorite(p, -1))
    
    def second(self, p):
        return self.get_nth_favorite(p,1)

    def play_animation(self, p, q, action):
        anims = []
        if self.G:
            anims += getattr(self.G, action)(p, q)
        if self.T:
            anims += getattr(self.T, action)(p, q)
        if self.scene:
            self.scene.play(*anims)

    def propose(self, p, q):
        self.play_animation(p, q, "propose")
        
    def reject(self, p, q):
        self.play_animation(p, q, "reject_proposal")
    
    def accept(self, p, q):
        self.play_animation(p, q, "accept_proposal")

    def symmetric_reject(self, p, q):
        if self.preferences[p][self.rank[p][q]] is not None:
            self.preferences[p][self.rank[p][q]] = None
            if self.scene and self.T:
                self.scene.play(*self.T.reject_proposal(p, q))
        if self.preferences[q][self.rank[q][p]] is not None:
            self.preferences[q][self.rank[q][p]] = None
            if self.scene and self.T:
                self.scene.play(*self.T.reject_proposal(q, p))

    def one_way_reject(self, p, q):
        self.play_animation(p, q, "reject_proposal")
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

            self.propose(p,top_pick)
            
            # top pick hasn't been proposed to yet, so they accept
            if accepted_proposal[top_pick] is None:
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
                self.one_way_reject(p, top_pick)
                first[p] += 1 # start at next spot
                continue # keep p in to_process
            
            # accept accepted_proposal, so old match has to return to their preference list again
            else: 
                self.one_way_reject(accepted_proposal[top_pick], top_pick)
                self.accept(p, top_pick)
                to_process.pop()
                # add old match to to_process
                to_process.append(accepted_proposal[top_pick])
                accepted_proposal[top_pick] = p
        
        # done processing, so everyone has gotten a proposal accepted
        return first, accepted_proposal

    def between_phases(self, proposals):
        for q in self.players:
            p = proposals[q] # q holds a proposal from p
            proposal_idx = self.rank[q][p]
            for r in self.original_preferences[q][proposal_idx+1:]:
                self.symmetric_reject(q, r)
                

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

    def find_second_favorite(self, p, first, last):
        count = 0
        pref = self.preferences[p]
        for j in range(first[p], len(self.preferences[p])):
            if pref[j] is not None:
                count += 1
            if count == 0:
                first[p] += 1
            if count == 2:
                return pref[j]
        return None

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

    def eliminate_rotation(self, p, q, first, last):
        for i in range(len(p)):
            # q_i rejects p_i so that p_i proposes to q_i+1, then q_i+1 rejects p_i+1 so that ...
            # q_0 rejects p_0 so that p_0 proposes to q_1, then q_1 rejects p_1 and accepts p_0 so that p_1 proposes to q_2, ...
            self.symmetric_reject(p[i], q[i])
            self.reject(p[i], q[i])
            if i > 0:
                self.accept(p[i-1], q[i])
            if i == len(p) - 1:
                self.propose(p[i], q[0])
                self.accept(p[i], q[0])
            else:
                self.propose(p[i], q[i+1])
            
            # all successors of p_i-1 are removed from q_i's list, and q_i is removed from their lists
            for j in range(self.rank[q[i]][p[i-1]]+1, last[q[i]]):
                reject = list(self.rank[q[i]].keys())[list(self.rank[q[i]].values()).index(j)]
                self.symmetric_reject(reject, q[i])
                
            last[q[i]] = self.rank[q[i]][p[i-1]]
