# ============================================================
#  CROP DISEASE PREDICTOR
#  Step 1 → Check if image is a plant
#  Step 2 → If yes, predict the disease
#  Step 3 → Show description, symptoms, and remedies
# ============================================================

import json
import numpy as np
import os
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image


# ============================================================
# STEP 1 — Load our disease model
# ============================================================

disease_model = load_model("models/phase1_best.h5")

# Load the list of disease names
with open("models/class_indices.json", "r") as f:
    class_indices = json.load(f)

# Flip it: { 0: "Tomato_blight", 1: "Corn_rust", ... }
disease_names = {v: k for k, v in class_indices.items()}

print("Disease model loaded!")


# ============================================================
# STEP 2 — Load MobileNet (used to check if image is a plant)
# ============================================================

plant_checker = MobileNetV2(weights="imagenet")

print("Plant checker loaded!")


# ============================================================
# STEP 3 — Load disease info from JSON
# ============================================================

with open("disease_info.json", "r") as f:
    disease_info = json.load(f)

print("Disease info loaded!")


# ============================================================
# STEP 4 — List of words that mean "plant"
# ============================================================

PLANT_WORDS = [
    "leaf", "plant", "flower", "tree", "herb",
    "vegetable", "fruit", "fern", "vine", "corn",
    "banana", "strawberry", "orange", "cucumber",
    "cabbage", "broccoli", "cauliflower", "rose",
    "daisy", "sunflower", "mushroom"
]


# ============================================================
# STEP 5 — Function to check if an image is a plant
# ============================================================

def check_if_plant(img_path):

    # Load and prepare the image
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    # Ask MobileNet: what is in this image?
    predictions = plant_checker.predict(img_array, verbose=0)
    top5 = decode_predictions(predictions, top=5)[0]

    # Check if any of the top 5 guesses sound like a plant
    for (_, label, _) in top5:
        for plant_word in PLANT_WORDS:
            if plant_word in label.lower():
                return True   # YES it's a plant

    return False  # NOT a plant


# ============================================================
# STEP 6 — Function to get disease info from JSON
# ============================================================

def get_disease_info(class_name):
    # Try exact match first
    if class_name in disease_info:
        return disease_info[class_name]
    
    # Normalize and try again
    # Removes extra underscores and brackets to find the best match
    def normalize(s):
        import re
        s = re.sub(r'_+', '_', s)        # collapse multiple underscores into one
        s = s.replace("(", "").replace(")", "")  # remove brackets
        s = s.strip("_")
        return s.lower()

    normalized_input = normalize(class_name)

    for key in disease_info:
        if normalize(key) == normalized_input:
            return disease_info[key]   # found a match!

    # Nothing matched at all
    return {
        "description": f"No information available for '{class_name}'.",
        "symptoms": ["Please consult an agricultural expert."],
        "remedies": ["Please consult an agricultural expert."]
    }

# ============================================================
# STEP 7 — Main predict function
# ============================================================

def predict(img_path):

    # Does the file exist?
    if not os.path.exists(img_path):
        print("Error: Image file not found!")
        return

    print("\n" + "=" * 55)
    print("Image:", img_path)
    print("=" * 55)

    # First, check if this is a plant image
    is_plant = check_if_plant(img_path)

    if not is_plant:
        print(" This is NOT a plant image.")
        print("   Please upload a photo of a plant leaf.")
        print("=" * 55 + "\n")
        return

    # It is a plant! Now predict the disease.
    print("Plant detected! Checking for disease...\n")

    # Load and prepare image for disease model
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Get predictions
    predictions = disease_model.predict(img_array, verbose=0)

    # Get top 3 results
    top3_indices = np.argsort(predictions[0])[::-1][:3]

    print("Top 3 Guesses:")
    for i, idx in enumerate(top3_indices):
        name = disease_names[idx]
        confidence = predictions[0][idx] * 100
        print(f"  {i+1}. {name:<45} {confidence:.2f}%")

    # ── Best guess ──────────────────────────────────────────
    best_idx   = top3_indices[0]
    best_class = disease_names[best_idx]
    best_conf  = predictions[0][best_idx] * 100
    readable   = best_class.replace("__", " - ").replace("_", " ").title()

    # ── Fetch info from JSON ─────────────────────────────────
    info = get_disease_info(best_class)

    # ── Display full result ──────────────────────────────────
    print("\n" + "=" * 55)
    print(f"  DISEASE  : {readable}")
    print(f"  CONFIDENCE: {best_conf:.2f}%")
    print("=" * 55)

    print(f"\n📋 DESCRIPTION")
    print(f"   {info['description']}")

    print(f"\n🔴 SYMPTOMS")
    for i, symptom in enumerate(info["symptoms"], 1):
        print(f"   {i}. {symptom}")

    print(f"\n✅ REMEDIES")
    for i, remedy in enumerate(info["remedies"], 1):
        print(f"   {i}. {remedy}")

    print("=" * 55 + "\n")



# — Run 


img_path = "new-plant-diseases-dataset/New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)/valid/Potato___Late_blight/0e068694-63b7-4edf-a93d-f2e9f28efaa6___RS_LB 3923.JPG"

predict(img_path)