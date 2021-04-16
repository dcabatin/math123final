from numpy.random import permutation
from irving_animator import IrvingAnimator
from irving_old import *
from player import *

def generate_sr_instance(players):
    players = set(players)
    preferences = {p :list(permutation(list(players - {p}))) for p in players}
    return preferences

def test():
    preferences = generate_sr_instance(range(6))
    players = players_from_pref_dict(preferences)
    S = IrvingAnimator(preferences)

    solver_result = S.match_roommates()
    oracle_result = stable_roommates(players)

    if solver_result is None and oracle_result is not None:
        return False, "Bad: no matching on instance with matching.", 0
    elif solver_result is None and oracle_result is None:
        return True, "Good: no matching on instance with no matching.", 0
    elif solver_result is not None and oracle_result is None:
        return False, "Bad: matching on instance with no matching!" , 1
    return True, "Good: matching on instance with matching.", 1

def runtest(n):
    tests = []
    acc = 0
    for _ in range(n):
        r, msg, m = test()
        acc += m
        if not r:
            print(msg)
        tests.append(r)

    print("All tests passed!" if all(tests) else "Tests failed.")
    return acc

if __name__ == "__main__":
    runtest(1000)