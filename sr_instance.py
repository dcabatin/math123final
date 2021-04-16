from numpy.random import permutation, choice, randint
from irving_solver import IrvingSolver
from irving_old import *
from player import *

def generate_sr_instance(players):
    players = set(players)
    preferences = {p :list(permutation(list(players - {p}))) for p in players}
    return preferences

def generate_incomplete_sr_instance(players):
    players = set(players)
    preferences = {p: list(choice(list(players - {p}), size=randint(len(players)-1), replace=False)) for p in players}
    return preferences

def test():
    preferences = generate_sr_instance(range(8))
    players = players_from_pref_dict(preferences)
    S = IrvingSolver(preferences)

    solver_result = S.match_roommates()
    oracle_result = stable_roommates(players)

    if solver_result is None and oracle_result is not None:
        return False, "Bad: no matching on instance with matching.", 0
    elif solver_result is None and oracle_result is None:
        return True, "Good: no matching on instance with no matching.", 0
    elif solver_result is not None and oracle_result is None:
        return False, "Bad: matching on instance with no matching!" , 1
    return True, "Good: matching on instance with matching.", 1

def test_incomplete():
    preferences = generate_incomplete_sr_instance(range(8))
    S = IrvingSolver(preferences)
    S.match_roommates()
    return True

def runtest(n):
    tests = []
    acc = 0
    for _ in range(n):
        r, msg, m = test()
        acc += m
        if not r:
            print(msg)
        tests.append(r)

    for _ in range(n):
        tests.append(test_incomplete())

    print("All tests passed!" if all(tests) else "Tests failed.")
    return acc

if __name__ == "__main__":
    runtest(1000)