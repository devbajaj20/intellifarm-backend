# 🌾 IntelliFarm Backend API
### AI-Powered Agricultural Decision Support System (Flask + ML + DL)

<p align="center">
  <img src="https://img.shields.io/badge/Backend-Flask-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/ML-ScikitLearn-green?style=for-the-badge">
  <img src="https://img.shields.io/badge/DL-TensorFlow-orange?style=for-the-badge">
  <img src="https://img.shields.io/badge/Deployment-Render-black?style=for-the-badge">
</p>

---

## 📌 Overview

This repository contains the **backend API service** for **IntelliFarm**, an intelligent agricultural platform that provides **real-time AI-driven recommendations** for farmers.

The backend is responsible for:
- Processing user inputs from the mobile app
- Running Machine Learning & Deep Learning models
- Returning predictions via REST APIs

---

## 🚀 Features

### 🌱 Crop Recommendation API
- Predicts best crop based on:
  - Nitrogen (N), Phosphorus (P), Potassium (K)
  - pH, Temperature, Humidity, Rainfall
- Model: Random Forest (high accuracy)

---

### 🧪 Fertilizer Recommendation API
- Suggests optimal fertilizer
- Detects nutrient deficiencies
- Uses encoded categorical + numerical features

---

### 🌿 Plant Disease Detection API
- Image-based prediction using CNN
- Input: Leaf image
- Output: Disease class + confidence

---

### ⚡ Real-Time ML Inference
- Fast API responses
- Pre-trained models loaded using Pickle / Keras

---

## 🏗️ Tech Stack

### 💻 Backend
- Python
- Flask (REST API)

### 🧠 Machine Learning
- Scikit-learn
- Random Forest, Decision Tree, SVM, KNN

### 🖼️ Deep Learning
- TensorFlow / Keras
- CNN Model (`.h5`)

### 📊 Data Processing
- Pandas
- NumPy

### ☁️ Deployment
- Render (Cloud Hosting)

---

## 🌐 Live API

👉 https://*********.onrender.com

---

## 🌐 Live Demo

👉 https://intellifarm-live.vercel.app/

⚡ Fully functional AI-powered agriculture platform

---

## 📂 Project Structure

```bash
intellifarm-backend/
│
├── app/
│   ├── routes.py              # API endpoints
│   ├── predict.py             # ML/DL prediction logic
│   ├── utils.py               # Helper functions
│
├── models/
│   ├── crop_model.pkl
│   ├── fertilizer_model.pkl
│   ├── disease_model.h5
│
├── encoders/
│   ├── soil_encoder.pkl
│   ├── crop_encoder.pkl
│   ├── fertilizer_encoder.pkl
│
├── data/
│   ├── crop_dataset.csv
│
├── training/
│   ├── train_crop_model.py
│   ├── train_fertilizer_model.py
│   ├── train_disease_model.py
│
├── requirements.txt
├── run.py                     # Entry point
└── README.md
