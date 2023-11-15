#!/bin/python3

from flask import Flask, render_template, jsonify
import json

HOST = "0.0.0.0"
PORT = "8000"
TEAMS_PATH = "teams.json"
MACHINES_PATH = "machines.json"
INDEX = "index.html"

app = Flask(__name__)

def get_current_scores():
    teams = {}
    machines = {}
    with open(TEAMS_PATH, "r") as t:
        teams = json.load(t)
    with open(MACHINES_PATH, "r") as m:
        machines = json.load(m)
    return (teams, machines)

@app.route("/")
def index():
    teams, machines = get_current_scores()
    return render_template(INDEX, teams=teams, machines=machines)

@app.route("/scores")
def scores():
    teams, machines = get_current_scores()
    return jsonify({"teams": teams, "machines": machines})


app.run(host="0.0.0.0", port=8000)