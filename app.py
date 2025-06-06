from flask import Flask, jsonify, request
from flask_cors import CORS
from pose_model import predict as predict_pose
from litter_model import predict_litter

app = Flask(__name__)
CORS(app)

THRESHOLD = 60.0

@app.route("/predict-pose", methods=["POST"])
def predict_pose_route():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    image = file.read()

    try:
        result = predict_pose(image)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    print(result)
    if result.get("probability", 0) < THRESHOLD:
        return jsonify({"class": "No chicken detected", "probability": 0.0})

    return jsonify(result)

@app.route("/predict-litter", methods=["POST"])
def predict_litter_route():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    image = file.read()

    try:
        result = predict_litter(image)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    print(result)
    if result.get("probability", 0) < THRESHOLD:
        return jsonify({"class": "No litter detected", "probability": 0.0})

    return jsonify(result)

# ✅ Add this health check route for Render to monitor the app
@app.route("/healthz")
def health_check():
    return "OK", 200

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

