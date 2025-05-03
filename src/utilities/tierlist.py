import uuid


class TierList:
    def __init__(self, size_tiers=5):
        self.name = None  # Defaults to null
        self.uuid = str(uuid.uuid4())
        self.game_session_id = None  # Defaults to null
        self.tiers = []  # eg, "S","A","B".
        self.images = []  # Each image is an s3 url, which will get rendered in html.

    # Returns the dictionary we will push into the mongodb collection.
    def to_dict(self):
        return {
            "uuid": self.uuid,
            "game_session_id": self.game_session_id,
            "name": self.name,
            "tiers": self.tiers,
            "images": self.images,
        }
