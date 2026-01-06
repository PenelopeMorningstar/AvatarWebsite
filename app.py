from flask import Flask, render_template, jsonify
import random
import time

app = Flask(__name__)

# ---- simple in-memory robot state (fake twin) ----
robot_state = {
    "speed": 0.0,          # units per second
    "steering": 0.0,       # -1 = left, 0 = straight, 1 = right
    "heading": 0.0,        # degrees
    "x": 0.0,
    "y": 0.0,
}

# Home page
@app.route("/")
def home():
    return render_template("index.html")


# API: robot status
@app.route("/api/status")
def robot_status():
    global robot_state

    # --- simulate speed ---
    speed_change = random.uniform(-0.3, 0.6)
    robot_state["speed"] = max(0, min(8, robot_state["speed"] + speed_change))

    # --- simulate steering ---
    if random.random() < 0.2:
        robot_state["steering"] = random.choice([-1, 0, 1])

    # --- update heading ---
    robot_state["heading"] += robot_state["steering"] * robot_state["speed"] * 0.8
    robot_state["heading"] %= 360

    # --- update position ---
    robot_state["y"] += robot_state["speed"] * 0.1
    robot_state["x"] += robot_state["steering"] * 0.05

    # --- simulate ultrasonic distances (cm) ---
    # Assuming 4 sensors: front, left, right, back
    obstacles = {
        "front": round(random.uniform(5, 200), 1),
        "left": round(random.uniform(5, 200), 1),
        "right": round(random.uniform(5, 200), 1),
        "back": round(random.uniform(5, 200), 1)
    }

    status = {
        "battery": f"{random.randint(60, 100)}%",
        "temperature": f"{random.randint(25, 38)}°C",
        "motors": "OK",
        "sensors": "OK",

        # motion data
        "speed": round(robot_state["speed"], 2),
        "steering": robot_state["steering"],   # -1, 0, 1
        "heading": round(robot_state["heading"], 1),
        "moving": robot_state["speed"] > 0.3,

        # position
        "position": {
            "x": round(robot_state["x"], 2),
            "y": round(robot_state["y"], 2)
        },

        # ultrasonic obstacles
        "obstacles": obstacles,

        "timestamp": time.time()
    }

    return jsonify(status)


if __name__ == "__main__":
    app.run(debug=True)
