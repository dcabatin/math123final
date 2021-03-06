from player import *

def _delete_pair(player, other):
    """Make a player forget another (and vice versa), deleting the pair from
    further consideration in the game."""

    player._forget(other)
    other._forget(player)


def first_phase(players):
    """Conduct the first phase of the algorithm where one-way proposals are
    made, and unpreferable pairs are forgotten."""

    free_players = players[:]
    while free_players:

        player = free_players.pop()
        
        favourite = player.get_favourite()

        current = favourite.matching
        if current is not None:
            favourite._unmatch()
            free_players.append(current)

        favourite._match(player)

        for successor in favourite.get_successors():
            _delete_pair(successor, favourite)
            if not successor.prefs and successor in free_players:
                free_players.remove(successor)

    return players


def locate_all_or_nothing_cycle(player):
    """Locate a cycle of (least-preferable, second-choice) pairs to be removed
    from the game."""

    lasts = [player]
    seconds = []
    while True:
        second_best = player.prefs[1]
        their_worst = second_best.prefs[-1]

        seconds.append(second_best)
        lasts.append(their_worst)

        player = their_worst

        if lasts.count(player) > 1:
            break

    idx = lasts.index(player)
    cycle = list(zip(lasts[idx + 1 :], seconds[idx:]))

    return cycle


def get_pairs_to_delete(cycle):
    """Based on an all-or-nothing cycle :math:`(x_1, y_1), \\ldots, (x_n, y_n)`,
    for each :math:`i = 1, \\ldots, n`, one must delete from the game all pairs
    :math:`(y_i, z)` such that :math:`y_i` prefers :math:`x_{i-1}` to :math:`z`
    where subscripts are taken modulo :math:`n`.
    This is an important point that is omitted from the original paper, but may
    be found in :cite:`GI89` (Section 4.2.3).
    The essential difference between this statement and that in :cite:`Irv85` is
    the removal of unpreferable pairs, identified using an all-or-nothing cycle,
    in addition to those contained in the cycle. Without doing so, tails of
    cycles can be removed rather than whole cycles, leaving some conflicting
    pairs in the game."""

    pairs = []
    for i, (_, right) in enumerate(cycle):

        left = cycle[(i - 1) % len(cycle)][0]
        successors = right.prefs[right.prefs.index(left) + 1 :]
        for successor in successors:
            pair = (right, successor)
            if pair not in pairs and pair[::-1] not in pairs:
                pairs.append((right, successor))

    return pairs


def second_phase(players):
    """Conduct the second phase of the algorithm where all-or-nothing cycles
    (rotations) are located and removed from the game."""

    player = next(p for p in players if len(p.prefs) > 1)
    while True:

        cycle = locate_all_or_nothing_cycle(player)
        pairs = get_pairs_to_delete(cycle)
        for player, other in pairs:
            _delete_pair(player, other)

        if any(p.prefs == [] for p in players):
            raise Exception()

        try:
            player = next(p for p in players if len(p.prefs) > 1)
        except StopIteration:
            break

    for player in players:
        player._unmatch()
        if player.prefs:
            player._match(player.get_favourite())

    return players


def stable_roommates(players):
    """Irving's algorithm :cite:`Irv85` that finds stable solutions to
    instances of SR if one exists. Otherwise, an incomplete matching is found.
    Parameters
    ----------
    players : list of Player
        The players in the game. Each must rank all other players.
    Returns
    -------
    matching : dict
        A dictionary of matches where the keys and values are given by the
        members of ``players``.
    """

    try:
        players = first_phase(players)

        if any(p.prefs == [] for p in players):
            raise Exception()

        if any(len(p.prefs) > 1 for p in players):
            players = second_phase(players)
    except Exception:
        return None

    matching = set()
    seen = set()
    for player in players:
        if player not in seen and player.matching not in seen:
            matching.add((player, player.matching))
        seen.add(player.matching)

    return matching

def matching_from_pref_dict(prefs):
    return stable_roommates(players_from_pref_dict(prefs))

test_preferences = {
    1: [3, 4, 2, 6, 5], 
    2: [6, 5, 4, 1, 3], 
    3: [2, 4, 5, 1, 6], 
    4: [5, 2, 3, 6, 1], 
    5: [3, 1, 2, 4, 6], 
    6: [5, 1, 3, 4, 2]}