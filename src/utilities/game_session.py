import uuid
from .tierlist import TierList
class GameSession:
    def __init__(self, players, tierlist: TierList):
        self.uuid = str(uuid.uuid4())
        self.anon = False # Anonimity, set false by default
        self.players = players
        self.tierlist = tierlist
        pass
