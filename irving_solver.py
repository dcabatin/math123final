from itertools import combinations
from copy import deepcopy
from preferences import *

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
        validate_incomplete_preferences(preferences)
        self.players = sorted(preferences.keys())
        self.n = len(self.players)
        self.preferences = deepcopy(preferences)
        self.original_preferences = deepcopy(preferences)
        self.adjacency = self.build_adjacency_matrix()
        self.prune_preferences()
        self.rank = self.build_ranking_matrix()
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
        return {p: set(self.preferences[p]) for p in self.players}
    
    def adjacent(self, p, q):
        return p in self.adjacency[q] and q in self.adjacency[p]

    def prune_preferences(self):
        for p in self.players:
            for i, q in enumerate(self.preferences[p]):
                if not self.adjacent(p,q):
                    self.preferences[p][i] = None

    def match_roommates(self):
        try:
            first, proposals = self.stable_roommates_phase_1()
            self.between_phases(proposals)

            last = {p: len(self.preferences[p]) - 1 for p in self.players}
            for p in self.players:
                while self.preferences[p][last[p]] is None:
                    last[p] -= 1
          
            self.stable_roommates_phase_2(first, last)
            self.clean_preferences(first, last)
            self.verify_solution(last)

            matches = set()
            visited = set()
            i = 0

            for p in self.players:
                if not p in visited:
                    pair = (p, self.preferences[p][last[p]])
                    visited.add(self.preferences[p][last[p]])
                    matches.add(pair)

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

    def symmetric_reject(self, p, q, play=True):
        if not self.adjacent(p,q):
            return
        self.preferences[p][self.rank[p][q]] = None
        self.preferences[q][self.rank[q][p]] = None

    def one_way_reject(self, p, q):
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
            self.symmetric_reject(p[i], q[i])                
            
            # all successors of p_i-1 are removed from q_i's list, and q_i is removed from their lists
            for j in range(self.rank[q[i]][p[i-1]]+1, last[q[i]]):
                reject = self.preferences[q[i]][j]
                self.symmetric_reject(reject, q[i])
                
            last[q[i]] = self.rank[q[i]][p[i-1]]