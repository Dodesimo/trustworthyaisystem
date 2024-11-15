from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

# AI Performance Table
ai_performance = [
    [0.95, 0.95, 0.95, 0.73, 0.95, 0.95, 0.73, 0.94, 0.95, 0.96],
    [0.95, 0.95, 0.95, 0.70, 0.95, 0.73, 0.73, 0.95, 0.96, 0.96],
    [0.95, 0.95, 0.94, 0.72, 0.70, 0.72, 0.56, 0.95, 0.96, 0.96],
    [0.95, 0.56, 0.95, 0.70, 0.68, 0.56, 0.57, 0.95, 0.95, 0.96],
    [0.56, 0.57, 0.68, 0.62, 0.94, 0.57, 0.95, 0.96, 0.94, 0.96],
    [0.57, 0.57, 0.68, 0.64, 0.94, 0.57, 0.95, 0.96, 0.95, 0.96],
    [0.96, 0.57, 0.70, 0.65, 0.94, 0.56, 0.57, 0.95, 0.95, 0.96],
    [0.96, 0.96, 0.68, 0.65, 0.94, 0.56, 0.57, 0.94, 0.96, 0.96],
    [0.96, 0.96, 0.69, 0.67, 0.70, 0.56, 0.56, 0.96, 0.96, 0.95],
    [0.96, 0.96, 0.72, 0.95, 0.72, 0.56, 0.56, 0.96, 0.96, 0.95]
]

# Human Performance Table
human_performance = [
    [0.90, 0.90, 0.90, 0.85, 0.90, 0.90, 0.75, 0.90, 0.90, 0.90],
    [0.90, 0.90, 0.90, 0.85, 0.90, 0.75, 0.75, 0.90, 0.90, 0.90],
    [0.90, 0.90, 0.90, 0.85, 0.85, 0.75, 0.75, 0.90, 0.90, 0.90],
    [0.90, 0.56, 0.90, 0.85, 0.70, 0.75, 0.75, 0.90, 0.90, 0.90],
    [0.75, 0.75, 0.75, 0.75, 0.90, 0.75, 0.95, 0.90, 0.90, 0.90],
    [0.57, 0.75, 0.75, 0.75, 0.90, 0.75, 0.95, 0.90, 0.90, 0.90],
    [0.90, 0.75, 0.85, 0.75, 0.90, 0.75, 0.75, 0.90, 0.90, 0.90],
    [0.90, 0.90, 0.75, 0.75, 0.90, 0.75, 0.75, 0.90, 0.90, 0.90],
    [0.90, 0.90, 0.75, 0.75, 0.85, 0.75, 0.75, 0.90, 0.90, 0.90],
    [0.90, 0.90, 0.85, 0.90, 0.85, 0.75, 0.75, 0.90, 0.90, 0.90]
]

# Terrain Type Table
surface_types = [
    ["Grassy", "Grassy", "Grassy", "Rocky", "Sandy", "Sandy", "Rocky", "Sandy", "Sandy", "Swampy"],
    ["Grassy", "Grassy", "Grassy", "Rocky", "Sandy", "Rocky", "Rocky", "Sandy", "Swampy", "Swampy"],
    ["Grassy", "Grassy", "Grassy", "Rocky", "Rocky", "Rocky", "Wooded", "Sandy", "Swampy", "Swampy"],
    ["Grassy", "Wooded", "Grassy", "Rocky", "Rocky", "Wooded", "Wooded", "Grassy", "Grassy", "Swampy"],
    ["Wooded", "Wooded", "Rocky", "Rocky", "Sandy", "Wooded", "Grassy", "Grassy", "Grassy", "Grassy"],
    ["Wooded", "Wooded", "Rocky", "Rocky", "Sandy", "Wooded", "Grassy", "Grassy", "Grassy", "Grassy"],
    ["Swampy", "Wooded", "Rocky", "Rocky", "Sandy", "Wooded", "Wooded", "Grassy", "Grassy", "Grassy"],
    ["Grassy", "Swampy", "Rocky", "Rocky", "Sandy", "Wooded", "Wooded", "Grassy", "Grassy", "Grassy"],
    ["Swampy", "Swampy", "Rocky", "Rocky", "Rocky", "Wooded", "Wooded", "Swampy", "Swampy", "Grassy"],
    ["Swampy", "Swampy", "Rocky", "Sandy", "Rocky", "Wooded", "Wooded", "Swampy", "Swampy", "Grassy"]
]

# State tracking
current_position = {'row': 0, 'col': 0}

@app.route("/")
def main():
    return render_template("dashboard.html")

@app.route("/get_state", methods=["GET"])
def get_state():
    row, col = current_position['row'], current_position['col']
    terrain_type = surface_types[row][col]
    ai_score = ai_performance[row][col]
    human_score = human_performance[row][col]
    return jsonify({"terrain_type": terrain_type, "ai_score": ai_score, "human_score": human_score})

@app.route("/advance", methods=["POST"])
def advance():
    row, col = current_position['row'], current_position['col']
    ai_score = ai_performance[row][col]
    human_score = human_performance[row][col]

    if ai_score > human_score:
        # Automated node traversal
        next_col = (col + 1) % 10
        next_row = row + 1 if next_col == 0 else row
        current_position['row'], current_position['col'] = next_row % 10, next_col
        return jsonify({"action": "auto", "next_row": current_position['row'], "next_col": current_position['col']})
    else:
        # Prompt user to manually check for mines
        return jsonify({"action": "manual"})

if __name__ == "__main__":
    app.run(debug=True)