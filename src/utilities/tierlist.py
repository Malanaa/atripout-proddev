import uuid


class TierList:
    def __init__(self, size_tiers=5):
        self.name = None  # Defaults to null
        self.uuid = str(uuid.uuid4())
        self.game_session_id = None  # Defaults to null
        self.tiers = []  # eg, "S","A","B".
        self.images = []  # Each image is an s3 url, which will get rendered in html.
        self.is_template = True
        self.user = None
    # Returns the dictionary we will push into the mongodb collection.
    def to_dict(self):
        return {
            "uuid": self.uuid,
            "game_session_id": self.game_session_id,
            "name": self.name,
            "tiers": self.tiers,
            "images": self.images,
            "is_template": self.is_template,
            "user": self.user
        }
    
    def syed(self):
        #  Make this into a seperate class that you can use to process tierlists.
        # each tierlist configuration lies as a vector in some N dimensional vector space.
        # we create a fucntion that gets the dot product of these vectors from anothwr arbitrary vector and 
        # so is cumalitve sum of all the dot products as a cost function which we then minize using our beloved
        # calculus 3 to find the average best configuration that satifies each part of the tierlist
        # visualzie this to get a better idea at whats going on 

        pass