from flask import Flask, render_template, url_for, request
from flask_socketio import SocketIO
from utilities import tierlist as tr
from utilities.mongodb.mongo_client import mongo_game_sessions, mongo_tierlists


# APP_OBJECT
app = Flask("__name__")
app.config['SECRET_KEY'] = 'temporary_please_do_not_forget_to_change!'
socketio = SocketIO(app)

@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")



@app.route('/sample_tierlist')
def sample_tierlist():
    sample_tierlist = tr.TierList()
    return render_template('sample_tierlist.html', tierlist=sample_tierlist)


if __name__ == '__main__':
    app.run()
    socketio.run(app)

