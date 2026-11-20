import json
import os
from datetime import datetime

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "scores.json")


def load_scores():

    #Read the list of results from the JSON file (empty list if missing)
    if not os.path.exists(DATA_FILE):
        return []
    
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_scores(scores):

    #Write the list of results to the JSON file
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(scores, f, ensure_ascii=False, indent=2)


@app.route("/")
def index():

    #The game page
    return render_template("index.html")


@app.route("/api/score", methods=["POST"])
def post_score():

    #Save the result of one game
    body = request.get_json(silent=True) or {}
    name = str(body.get("name", "")).strip()
    score = body.get("score")

    if not name or not isinstance(score, int):
        return jsonify({"error": "Name and score are required."}), 400

    scores = load_scores()
    scores.append({
        "name": name[:15],
        "score": score,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
    })
    save_scores(scores)

    return jsonify({"ok": True}), 201


@app.route("/api/leaderboard", methods=["GET"])
def get_leaderboard():
    
    #Return the 10 best results, highest first
    scores = sorted(load_scores(), key=lambda s: s["score"], reverse=True)
    
    return jsonify({"leaderboard": scores[:10]})


if __name__ == "__main__":
    app.run(debug=True)
