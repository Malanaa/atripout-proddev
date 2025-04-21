import uuid

DEFAULT_TIERS = ['S', 'A', 'B', 'C', 'D']
class TierList:
    def __init__(self, size_tiers = 5):
        self.uuid = str(uuid.uuid4())
        self.size_tiers = 5 # DEFAULT NUMBER OF TIERS
        self.tiers = {DEFAULT_TIERS[i]: [] for i in range(len(DEFAULT_TIERS))}
        self.images = []

    def place_holder():
        pass


