import uuid
import random


class GameSession:
    def __init__(self, num_players):
        self.game_session_id = str(uuid.uuid4())
        self.room_id = f"{random.randint(0, 999999):06d}"
        self.num_players = num_players
        self.tierlist_id = None
        self.users = []

    def to_dict(self):
        return {
            "game_session_id": self.game_session_id,
            "room_id": self.room_id,
            "num_players": self.num_players,
            "tierlist_uuid": self.tierlist_id,
            "users": self.users
        }
