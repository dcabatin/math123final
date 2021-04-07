class Player:
    """A base class to represent a player within a matching game.
    Parameters
    ----------
    name : object
        An identifier. This should be unique and descriptive.
    Attributes
    ----------
    prefs : List[Player]
        The player's preferences. Defaults to ``None`` and is updated using the
        ``set_prefs`` method.
    matching : Optional[Player]
        The current match of the player. ``None`` if not currently matched.
    _pref_names : Optional[List]
        A list of the names in ``prefs``. Updates with ``prefs`` via
        ``set_prefs`` method.
    _original_prefs : Optional[List[Player]]
        The original set of player preferences. Defaults to ``None`` and does
        not update after the first ``set_prefs`` method call.
    """

    def __init__(self, name):

        self.name = name
        self.prefs = []
        self.matching = None

        self._pref_names = []
        self._original_prefs = None

    def __repr__(self):

        return str(self.name)

    def _forget(self, other):
        """Forget another player by removing them from the player's preference
        list."""

        prefs = self.prefs[:]
        prefs.remove(other)
        self.prefs = prefs

    def unmatched_message(self):

        return f"{self} is unmatched."

    def not_in_preferences_message(self, other):

        return (
            f"{self} is matched to {other} but they do not appear in their "
            f"preference list: {self.prefs}."
        )

    def set_prefs(self, players):
        """ Set the player's preferences to be a list of players. """

        self.prefs = players
        self._pref_names = [player.name for player in players]

        if self._original_prefs is None:
            self._original_prefs = players[:]

    def prefers(self, player, other):
        """Determines whether the player prefers a player over some other
        player."""

        prefs = self._original_prefs
        return prefs.index(player) < prefs.index(other)

    def _match(self, other):
        """ Assign the player to be matched to some other player. """

        self.matching = other

    def _unmatch(self):
        """ Set the player to be unmatched. """

        self.matching = None

    def get_favourite(self):
        """ Get the player's favourite player. """

        return self.prefs[0]

    def get_successors(self):
        """ Get all the successors to the current match of the player. """

        idx = self.prefs.index(self.matching)
        return self.prefs[idx + 1 :]

    def check_if_match_is_unacceptable(self, unmatched_okay=False):
        """Check the acceptability of the current match, with the stipulation
        that being unmatched is okay (or not)."""

        other = self.matching

        if other is None and unmatched_okay is False:
            return self.unmatched_message()

        elif other is not None and other not in self.prefs:
            return self.not_in_preferences_message(other)

def players_from_pref_dict(prefs):
    players = {i: Player(i) for i in prefs.keys()}
    fixed_preferences = {i: [players[j] for j in prefs[i]] for i in prefs.keys()}
    for (k,v) in fixed_preferences.items():
        players[k].set_prefs(v)
    return list(players.values())