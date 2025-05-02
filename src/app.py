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

# APP_OBJECT
app = Flask("__name__")
app.config["SECRET_KEY"] = "temporary_please_do_not_forget_to_change!"
socketio = SocketIO(app)


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/create", methods=["POST", "GET"])
def create_game():
    if request.method == "POST":
        player_number = request.form.get("playerNumber")
        anonymous = request.form.get("anonymous") == "yes"
        return redirect(
            url_for("tierlist_proccessing", isAnon=anonymous, numPlayers=player_number)
        )
    # send tierlistobjects and like set up a tierlits room.
    return render_template("create_game.html")


# Im unsure if this will work, but I dont thinkj I always need static names.
@app.route(f"/tierlist-processing", methods=["POST", "GET"])
def tierlist_proccessing():
    is_anon = request.args.get("isAnon")
    num_players = request.args.get("numPlayers")
    tierlist = tr.TierList()
    if request.method == "POST":
        # game_session = gs.GameSession(num_players, tierlist)
        # game_session.anon = is_anon

        # Byte64 image array
        images = request.files.getlist("images[]")
        tiernames = request.form.getlist("tier_names[]")
        
        tierlist.tiers = tiernames
        tierlist.size_tiers = len(tiernames)

        tierlist_id = mongo_tierlists.insert_one(tierlist.to_dict()).inserted_id
        # saving the images to s3
        for file in images:
            img_io_in = io.BytesIO(file.read()) 
            img = Image.open(img_io_in)
            img = img.convert("RGB")
            img_io_out = io.BytesIO()
            img.save(img_io_out, format="JPEG", quality=85, optimize=True)
            img_io_out.seek(0)

            unique_key = (uuid.uuid4())
            s3.upload_fileobj(
            img_io_out,
            "atripout-images",
            unique_key,
            ExtraArgs={
            "ACL": "public-read",
            "ContentType": "image/jpeg", #Jpeg specifier
            },
            )
            s3_url = f"https://atripout-images.s3.us-east-2.amazonaws.com/{unique_key}"
            mongo_tierlists.update_one({"_id": tierlist_id}, {"$set": {"image_url": s3_url}})

        print(len(tiernames), len(images))  


        # get all relevant data to attach to the teirlist which then u attach to the game session
        # request.form.get()
        pass
    return render_template("middleman_tierlist.html")


# Defining n-directional sockets (socketio rooms)
@socketio.on("join_room")
def on_join(data):
    username = data["username"]
    room = data["room"]
    join_room(room)  # I assume this is some sort of uid for each room sepratly
    emit("room_response", f"{username} has joined session = {room}", to=room)
    print(f"{username} has joined {room}")


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


@app.route("/test")
def test():
    return render_template("home.html")


@app.route("/join")
def join_game():
    return render_template("index.html")


@app.route("/sample_tierlist")
def sample_tierlist():
    sample_tierlist = tr.TierList()
    return render_template("sample_tierlist.html", tierlist=sample_tierlist)


@socketio.on("send_text_to_server")
def handle_test_send_event(msg):
    print(f"message from client: {msg}")
    time.sleep(2)
    socketio.emit("send_text_to_client", input(f"{msg}: "))


# @socketio.on('message')
# def handle_message(msg):
#     print(f"Logged Message : {msg}")
#     socketio.emit('second_response', {'data': 'Message received!'})

# @socketio.on('gang')
# def handle_gang(msg):
#     print(f"gang messagiung wow : {msg}")
#     socketio.emit('response', {'data': 'GANG Message received!'})
# if __name__ == '__main__':
#     socketio.run(app)
