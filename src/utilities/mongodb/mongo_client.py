import pymongo
from dotenv import load_dotenv
import os
import certifi

load_dotenv()
mongo_connection_string = os.getenv("CUSTOMCONNSTR_MONGO_CONNECTION_STRING")
# Mongo Connection Client Via Connection String Atlas, this is somewhat deprecated since I don't plan on
# using azure, but lets keep the convention going for now.
client = pymongo.MongoClient(mongo_connection_string, tlsCAFile=certifi.where())

# Prod01c : Current Production DB
prod01c = client["prod01c"]

# Tierlists
mongo_tierlists = prod01c["tierlists"]

# Games
mongo_game_sessions = prod01c["sessions"]
