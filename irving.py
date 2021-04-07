class IrvingSolver():
    
    test_preferences = {
        1: [3, 4, 2, 6, 5], 
        2: [6, 5, 4, 1, 3], 
        3: [2, 4, 5, 1, 6], 
        4: [5, 2, 3, 6, 1], 
        5: [3, 1, 2, 4, 6], 
        6: [5, 1, 3, 4, 2]}

    def __init__(self, preferences=test_preferences):
        self.players = sorted(preferences.keys())
        self.n = len(self.players)
        self.preferences = preferences
        self.rank = self.get_ranking_matrix()

    def get_ranking_matrix(self):
        rank = {p : { q: None for q in self.preferences[p]} for p in self.players}

        for p in self.players:
            for j in range(len(self.preferences[p])):
                idx = self.preferences[p][j]
                rank[p][idx] = j
        
        return rank

    def match_roommates(self):
        first, last = self.stable_roommates_phase_1()
        self.stable_roommates_phase_2(first, last)
        self.clean_preferences(first, last)

        matches = []
        visited = set()
        i = 0
        
        for p in self.players:
            if not p in visited:
                pair = (p, self.preferences[p][last[p]])
                visited.add(self.preferences[p][last[p]])
                visited.add(p)
                matches.append(pair)
        
        return matches

    def stable_roommates_phase_1(self):
        proposal = {p: None for p in self.players}
        first = {p: 0 for p in self.players}
        last = {p: len(self.preferences[p]) for p in self.players}
        to_process = list(self.players)
        
        while len(to_process) > 0:
            p = to_process[0]
            
            # update first pointer if necessary
            while self.preferences[p][first[p]] == None:
                first[p] += 1
                
            top_pick = self.preferences[p][first[p]]
            
            # top pick hasn't been proposed to yet, so they accept
            if proposal[top_pick] == None:
                proposal[top_pick] = p
                
                match_rank = self.preferences[top_pick].index(p)
                
                # all candidates worse than i are rejected, must remove top_pick from their preference list
                for idx in range(match_rank+1, last[top_pick]):
                    reject = self.preferences[top_pick][idx]
                    self.preferences[reject][self.rank[reject][top_pick]] = None
                
                # update last pointer
                last[top_pick] = match_rank
                del to_process[0]
                
                continue
            
            curr_match_idx = self.rank[top_pick][proposal[top_pick]]
            potential_match_idx = self.rank[top_pick][p]
            
            if curr_match_idx < potential_match_idx: # current matching is preferred, i is rejected
                self.preferences[top_pick][potential_match_idx] = None
                
                first[p] += 1 # start at next spot
                
                continue
            
            else: # accept proposal, so old match has to return to their preference list again
                self.preferences[top_pick][curr_match_idx] = None
                
                # old match is rejected by top_pick, must update their list
                top_pick_idx = self.rank[proposal[top_pick]][top_pick]
                self.preferences[proposal[top_pick]][top_pick_idx] = None
                
                del to_process[0]
                # add old match to to_process
                to_process.insert(0, proposal[top_pick])
                
                proposal[top_pick] = p
                last[top_pick] = potential_match_idx
        
        return first, last

    def clean_preferences(self, first, last):
        for p in self.players:
            for j in range(len(self.preferences[p])):
                if j < first[p] or j > last[p]:
                    self.preferences[p][j] = None

    def stable_roommates_phase_2(self, first, last):
        while True:
            p, q = None, None
            # find first p_0 to get a rotation from
            # preference list of p_0 must contain at least 2 elements
            for p_0 in self.players:
                if last[p_0] - first[p_0] > 0 and self.find_second_favorite(p_0, first, last) != None:
                    p, q = self.find_rotation(0, [p_0], [None], first, last)
                    break
            
            if not p and not q:
                return
            
            # eliminate rotation
            self.eliminate_rotation(p, q, first, last)

    def find_second_favorite(self, p, first, last):
        count = 0
        pref = self.preferences[p]
        for j in range(first[p], last[p]+1):
            if not pref[j] == None:
                count += 1
            elif count == 0:
                first[p] += 1
            if count == 2:
                return pref[j]
        return None

    def find_rotation(self, i, p, q, first, last):
        second_favorite = self.find_second_favorite(p[i], first, last)
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
            # q_i rejects p_i so that p_i proposes to q_i+1
            self.preferences[p[i]][self.rank[p[i]][q[i]]] = None
            
            # all successors of p_i-1 are removed from q_i's list, and q_i is removed from their lists
            for j in range(self.rank[q[i]][p[i-1]]+1, last[q[i]]):
                reject = list(self.rank[q[i]].keys())[list(self.rank[q[i]].values()).index(j)]
                #reject = self.rank[q[i]].index(j) #preferences[q[i]][j]
                self.preferences[reject][self.rank[reject][q[i]]] = None
                
            last[q[i]] = self.rank[q[i]][p[i-1]]