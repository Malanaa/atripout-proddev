import uuid
import random
from .tierlist import TierList


class GameSession:
    def __init__(self, num_players, tierlist: TierList):
        self.game_session_id = str(uuid.uuid4())
        self.room_id = f"{random.randint(0, 999999):06d}"
        self.anonymous = False  # Anonimity, set false by default.
        self.num_players = num_players
        self.tierlist = tierlist
        pass

    def to_dict(self):
        return {
            "game_session_id": self.game_session_id,
            "room_id": self.room_id,
            "anonymous": self.anonymous,
            "num_players": self.num_players,
            "tierlist_uuid": self.tierlist.uuid,
        }
