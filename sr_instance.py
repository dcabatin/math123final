from numpy.random import permutation
from irving import IrvingSolver
from irving_old import *
from player import *

def generate_sr_instance(players):
    players = set(players)
    preferences = {p :list(permutation(list(players - {p}))) for p in players}
    return preferences

def test():
    preferences = generate_sr_instance(range(8))
    players = players_from_pref_dict(preferences)
    S = IrvingSolver(preferences)

    solver_result = S.match_roommates()
    oracle_result = stable_roommates(players)

    if solver_result is None and oracle_result is not None:
        return False, "Bad: no matching on instance with matching."
    elif solver_result is None and oracle_result is None:
        return True, "Good: no matching on instance with no matching."
    elif solver_result is not None and oracle_result is None:
        return False, "Bad: matching on instance with no matching!" 
    return True, "Good: matching on instance with matching."

tests = []

for _ in range(10000):
    r, msg = test()
    if not r:
        print(msg)
    tests.append(r)

print(all(tests))