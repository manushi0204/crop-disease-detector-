
from base import app
from flask import render_template,redirect,session
# import base.com.controller.crop_controller
#
#
# @app.route('/')
# def index():
#     return render_template("base/templates/admin/login.html")
#
#
# @app.route('/userDetails')
# def userDetails():
#     from base.com.dao.user_dao import UserDAO
#     user_dao = UserDAO()
#     user_list = user_dao.view_all_users()
#     return render_template("base/templates/admin/viewUsers.html", user_list=user_list)
#
#

#
#

#
#
if __name__ == '__main__':

# ============================================================
#  CROPDOCTOR — Flask Backend
#  Every prediction is saved to MySQL automatically
# ============================================================

import json
import numpy as np
import os
import re
import mysql.connector
from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)

# Folder where uploaded images will be saved temporarily
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ============================================================
# LOAD MODELS AND DATA
# ============================================================

disease_model = load_model("models/phase1_best.h5")

with open("models/class_indices.json", "r") as f:
    class_indices = json.load(f)
disease_names = {v: k for k, v in class_indices.items()}

with open("disease_info.json", "r") as f:
    disease_info = json.load(f)

plant_checker = MobileNetV2(weights="imagenet")

print("All models and data loaded!")


# ============================================================
# MYSQL CONNECTION
# ============================================================

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",       
        password="root",
        database="cropdoctor"
    )


# ============================================================
# HELPER — Save prediction to MySQL
# ============================================================

def save_to_db(image_name, disease_name, confidence, description, symptoms, remedies):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO predictions
                (image_name, disease_name, confidence, description, symptoms, remedies)
            VALUES
                (%s, %s, %s, %s, %s, %s)
        """
        # Store symptoms and remedies as JSON strings in the TEXT column
        values = (
            image_name,
            disease_name,
            round(confidence, 2),
            description,
            json.dumps(symptoms),
            json.dumps(remedies)
        )

        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Saved to DB: {disease_name} ({confidence:.2f}%)")

    except Exception as e:
        print(f"DB Error: {e}")


# ============================================================
# HELPER — Check if image is a plant
# ============================================================

PLANT_WORDS = [
    "leaf", "plant", "flower", "tree", "herb",
    "vegetable", "fruit", "fern", "vine", "corn",
    "banana", "strawberry", "orange", "cucumber",
    "cabbage", "broccoli", "cauliflower", "rose",
    "daisy", "sunflower", "mushroom"
]

def check_if_plant(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    predictions = plant_checker.predict(img_array, verbose=0)
    top5 = decode_predictions(predictions, top=5)[0]

    for (_, label, _) in top5:
        for plant_word in PLANT_WORDS:
            if plant_word in label.lower():
                return True
    return False


# ============================================================
# HELPER — Get disease info from JSON (with fuzzy matching)
# ============================================================

def normalize(s):
    s = re.sub(r'_+', '_', s)
    s = s.replace("(", "").replace(")", "")
    s = s.strip("_")
    return s.lower()

def get_disease_info(class_name):
    if class_name in disease_info:
        return disease_info[class_name]

    normalized_input = normalize(class_name)
    for key in disease_info:
        if normalize(key) == normalized_input:
            return disease_info[key]

    return {
        "description": f"No information available for '{class_name}'.",
        "symptoms": ["Please consult an agricultural expert."],
        "remedies": ["Please consult an agricultural expert."]
    }


# ============================================================
# ROUTE — POST /predict
# ============================================================

@app.route("/predict", methods=["POST"])
def predict():

    # Check if image was sent
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    # Save the uploaded image temporarily
    filename = secure_filename(file.filename)
    img_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(img_path)

    # Step 1 — Check if it's a plant
    if not check_if_plant(img_path):
        os.remove(img_path)
        return jsonify({
            "error": "Not a plant image",
            "message": "Please upload a photo of a plant leaf."
        }), 400

    # Step 2 — Predict disease
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    preds = disease_model.predict(img_array, verbose=0)
    top3_indices = np.argsort(preds[0])[::-1][:3]

    best_idx    = top3_indices[0]
    best_class  = disease_names[best_idx]
    best_conf   = float(preds[0][best_idx]) * 100
    readable    = best_class.replace("__", " - ").replace("_", " ").title()

    # Step 3 — Get disease info
    info = get_disease_info(best_class)

    # Step 4 — Save to MySQL
    save_to_db(
        image_name   = filename,
        disease_name = readable,
        confidence   = best_conf,
        description  = info["description"],
        symptoms     = info["symptoms"],
        remedies     = info["remedies"]
    )

    # Step 5 — Build top 3 list for response
    top3 = []
    for idx in top3_indices:
        top3.append({
            "disease": disease_names[idx].replace("__", " - ").replace("_", " ").title(),
            "confidence": f"{preds[0][idx] * 100:.2f}%"
        })

    # Step 6 — Return JSON response
    return jsonify({
        "image"      : filename,
        "disease"    : readable,
        "confidence" : f"{best_conf:.2f}%",
        "description": info["description"],
        "symptoms"   : info["symptoms"],
        "remedies"   : info["remedies"],
        "top3"       : top3,
        "saved_to_db": True
    }), 200


# ============================================================
# ROUTE — GET /history
# (Returns all past predictions from the database)
# ============================================================

@app.route("/history", methods=["GET"])
def history():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM predictions ORDER BY predicted_at DESC")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        # Parse symptoms and remedies back from JSON strings
        for row in rows:
            row["symptoms"] = json.loads(row["symptoms"])
            row["remedies"] = json.loads(row["remedies"])
            row["predicted_at"] = str(row["predicted_at"])

        return jsonify({"total": len(rows), "predictions": rows}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    app.run(debug=True)