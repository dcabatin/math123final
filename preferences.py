char_test_preferences = {
    'a': ['c', 'd', 'b', 'f', 'e'], 
    'b': ['f', 'e', 'd', 'a', 'c'], 
    'c': ['b', 'd', 'e', 'a', 'f'], 
    'd': ['e', 'b', 'c', 'f', 'a'], 
    'e': ['c', 'a', 'b', 'd', 'f'], 
    'f': ['e', 'a', 'c', 'd', 'b']}

phase_2_unsat_preferences = {
    0: [4, 1, 3, 5, 2], 
    1: [4, 5, 0, 3, 2], 
    2: [0, 1, 5, 3, 4], 
    3: [4, 2, 0, 5, 1], 
    4: [5, 2, 1, 0, 3], 
    5: [1, 4, 0, 3, 2]}

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

incomplete_preferences = {
    1: [2,3],
    2: [1,3,4],
    3: [4,1,2],
    4: [3]
}

incomplete_preferences2 = {
    1: [3, 4, 2, 6, 5], 
    2: [6, 4, 1, 3], 
    3: [4, 5, 6], 
    4: [5, 2, 6, 1], 
    5: [3, 1, 2, 4, 6], 
    6: [5, 1]}