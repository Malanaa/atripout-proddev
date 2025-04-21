from flask import Flask, render_template, url_for, request
from utilities import tierlist as tr

app = Flask("__name__")

@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")


@app.route('/sample_tierlist')
def sample_tierlist():
    sample_tierlist = tr.TierList()
    return render_template('sample_tierlist.html', tierlist=sample_tierlist)

