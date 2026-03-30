
from base import app, db
from base.com.vo.crop_vo import CropVO
from base.com.vo.disease_vo import DiseaseVO

with app.app_context():
    db.session.query(DiseaseVO).delete()
    db.session.query(CropVO).delete()
    db.session.commit()
    print("All test data cleaned!")

import json
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# ==========================
# LOAD BEST MODEL
# ==========================

model = load_model("models/phase1_best.h5")

with open("models/class_indices.json", "r") as f:
    class_indices = json.load(f)

index_to_class = {v: k for k, v in class_indices.items()}

print(f"Model loaded. Total classes: {len(index_to_class)}")

# ==========================
# TEST DATA — using valid folder
# ==========================

TEST_PATH = "new-plant-diseases-dataset/New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)/valid"

IMG_SIZE = (224, 224)
BATCH_SIZE = 32

test_datagen = ImageDataGenerator(rescale=1./255)

test_generator = test_datagen.flow_from_directory(
    TEST_PATH,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    shuffle=False
)

# ==========================
# OVERALL ACCURACY
# ==========================

print("\nEvaluating model...")
loss, accuracy = model.evaluate(test_generator, verbose=1)
print(f"\nTest Loss    : {loss:.4f}")
print(f"Test Accuracy: {accuracy * 100:.2f}%")

# ==========================
# PER CLASS ACCURACY
# ==========================

print("\nCalculating per-class accuracy...")
predictions = model.predict(test_generator, verbose=1)
predicted_indices = np.argmax(predictions, axis=1)
true_indices = test_generator.classes

correct = predicted_indices == true_indices

print(f"\n{'Class':<45} {'Correct':>7} {'Total':>7} {'Accuracy':>9}")
print("=" * 72)

for class_idx in range(len(index_to_class)):
    class_name = index_to_class[class_idx]
    class_mask = true_indices == class_idx
    class_correct = correct[class_mask].sum()
    class_total = class_mask.sum()
    class_acc = (class_correct / class_total * 100) if class_total > 0 else 0
    print(f"{class_name:<45} {class_correct:>7} {class_total:>7} {class_acc:>8.2f}%")

print("=" * 72)
print(f"{'Overall':<45} {correct.sum():>7} {len(correct):>7} {accuracy*100:>8.2f}%")

