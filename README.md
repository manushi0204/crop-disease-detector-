# crop-disease-detector-

🌿 Crop Disease Detector
An AI-powered web application that detects plant leaf diseases from uploaded images using deep learning.

📌 What It Does

User uploads a photo of a plant leaf
A MobileNetV2 plant filter first checks if the image is actually a plant
If it is a plant, a fine-tuned MobileNetV2 disease model detects the disease
The result page shows the disease name, confidence score, cause, and treatment
Admin panel lets admins manage users and view all predictions


🧠 Model Details
ModelPurposeMobileNetV2 (fine-tuned)Disease detection — trained on 38 plant disease classesMobileNetV2 (ImageNet)Plant filter — rejects non-plant images like humans or objects

Dataset: New Plant Diseases Dataset (Augmented) from Kaggle
Classes: 38 (covers diseases across Tomato, Corn, Potato, Apple, Grape and more)
Input size: 224 × 224
Training: Done on Google Colab
