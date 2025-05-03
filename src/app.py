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
        is_anonymous = request.form.get("anonymous") == "yes"
        # Redirects to a middleman endpoint which initializes the tierlist and gamesession.
        return redirect(
            url_for(
                "tierlist_proccessing", is_anon=is_anonymous, player_num=player_number
            )
        )
    return render_template("create_game.html")


@app.route("/desgin_x11c", methods=["POST", "GET"])
def tierlist_proccessing():
    is_anon = request.args.get("is_anon")
    num_players = request.args.get("player_num")

    if request.method == "POST":

        tierlist = tr.TierList()

        game_session = gs.GameSession(num_players, tierlist)
        game_session.anonymous = is_anon

        # Reading in the data from the post request.
        images = request.files.getlist("images[]")
        tiernames = request.form.getlist("tier_names[]")
        tierlist_name = request.form.get("tierlist_name")

        print(tierlist_name)
        # Tierlist customization.
        tierlist.tiers = tiernames
        tierlist.name = tierlist_name
        tierlist_id = mongo_tierlists.insert_one(tierlist.to_dict()).inserted_id

        # Saving every image to s3, while adding them to the tierlists image array.
        if len(images) > 0:
            # somewhat redundant, but lets let it be.
            for file in images:

                # "null" check.
                if file.filename == "" or file.content_length == 0:
                    continue

                img_io_in = io.BytesIO(file.read())
                if img_io_in.getbuffer().nbytes == 0:
                    continue

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
                s3_url = (
                    f"https://atripout-images.s3.us-east-1.amazonaws.com/{unique_key}"
                )
                mongo_tierlists.update_one(
                    {"_id": tierlist_id}, {"$push": {"images": s3_url}}
                )
        # Resetting images because I think it's holding data.
        images = []
        return redirect(url_for("home"))
    return render_template("tier_proccesing.html")


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
