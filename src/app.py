from flask import Flask, render_template, url_for, request, redirect
from flask_socketio import SocketIO, join_room, leave_room, emit
from utilities import tierlist as tr
from utilities import game_session as gs
from utilities.mongodb.mongo_client import mongo_game_sessions, mongo_tierlists
from utilities.s3bucket.s3_config import s3
import eventlet as et
import time
import uuid
from PIL import Image
import io


app = Flask("__name__")
app.config["SECRET_KEY"] = "temp"  # Change to secure string stored in dotenv.
socketio = SocketIO(app)


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/create", methods=["POST", "GET"])
def create_game():
    if request.method == "POST":
        player_number = request.form.get("playerNumber")
        # Redirects to a middleman endpoint which initializes the tierlist and gamesession.
        return redirect(
            url_for(
                "tierlist_proccessing", num_players=player_number
            )
        )
    return render_template("create_game.html")


@app.route("/desgin_x11c", methods=["POST", "GET"])
def tierlist_proccessing():

    num_players = request.args.get("num_players")
    print(num_players)

    # As issue occurs, when the user enters no images. Fix pending.
    if request.method == "POST":

        num_players = request.form.get("num_players")
        tierlist = tr.TierList()
        game_session = gs.GameSession(num_players)

        # Reading in the data from the post request.
        images = request.files.getlist("images[]")
        tiernames = request.form.getlist("tier_names[]")
        tierlist_name = request.form.get("tierlist_name")

        # Tierlist customization.
        tierlist.tiers = tiernames
        tierlist.name = tierlist_name
        tierlist_id = mongo_tierlists.insert_one(tierlist.to_dict()).inserted_id
        tierlist.game_session_id = game_session.game_session_id

        # Game Session Customization
        game_session.tierlist_id = tierlist.uuid
        game_session.num_players = num_players


        for file in images:
            img_io_in = io.BytesIO(file.read())
            img = Image.open(img_io_in)
            img = img.convert("RGB")
            img_io_out = io.BytesIO()
            img.save(img_io_out, format="JPEG", quality=85, optimize=True)
            img_io_out.seek(0)

            unique_key = str(uuid.uuid4())
            s3.upload_fileobj(
                img_io_out,
                "atripout-images",
                unique_key,
                ExtraArgs={
                    "ACL": "public-read",
                    "ContentType": "image/jpeg",  # JPEG specifier.
                },
            )
            s3_url = f"https://atripout-images.s3.us-east-1.amazonaws.com/{unique_key}"
            mongo_tierlists.update_one(
                {"_id": tierlist_id}, {"$push": {"images": s3_url}}
            )
        mongo_game_sessions.insert_one(game_session.to_dict())
        return redirect(
            url_for(
                "lobby",
                game_session_id=game_session.game_session_id,
                tierlist_uuid=tierlist.uuid,
            )
        )
    return render_template("tier_proccesing.html", num_players=num_players)


@app.route("/lobby", methods=["POST", "GET"])
def lobby():
    game_session_id = request.args.get("game_session_id")
    game_session = mongo_game_sessions.find_one({"game_session_id": game_session_id})
    tierlist_uuid = request.args.get("tierlist_uuid")
    tierlist = mongo_tierlists.find_one({"uuid": tierlist_uuid})
    return render_template("lobby.html", game_session=game_session, tierlist=tierlist)


# Defining n-directional sockets (socketio rooms)
@socketio.on("join_room")
def on_join(data):
    username = data["username"]
    room = data["room"]
    join_room(room)  # I assume this is some sort of uid for each room sepratly
    emit("room_response", f"{username} has joined session = {room}", to=room)
    print(f"{username} has joined {room}")


# Under Works
@app.route("/join")
def join_game():
    return render_template("index.html")


# Sockets Handling


# Room Based Socket Netowrking
@socketio.on("leave_room")
def on_leave(data):
    username = data["username"]
    room = data["room"]
    leave_room(room)
    emit("room_response", f"{username} has left the room {room}.", to=room)
    print(f"{username} has left the room {room}.")


@socketio.on("send_message_to_room")
def handle_send_message(data):
    room = data["room"]
    message = data["message"]
    emit("room_message", message, to=room)


# General Based Socket Netowrking
@socketio.on("send_text_to_server")
def handle_test_send_event(msg):
    print(f"message from client: {msg}")
    time.sleep(2)
    socketio.emit("send_text_to_client", input(f"{msg}: "))
