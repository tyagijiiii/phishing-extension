import os
import joblib
import pandas as pd
import urllib.parse
from flask import Flask, request, jsonify
from sklearn.preprocessing import StandardScaler

# ✅ Load Random Forest Model
RF_MODEL_PATH = "random_forest_model.pkl"

if os.path.exists(RF_MODEL_PATH):
    rf_model = joblib.load(RF_MODEL_PATH)
    print("✅ Random Forest Model Loaded Successfully!")
else:
    raise FileNotFoundError(f"❌ {RF_MODEL_PATH} not found. Train and save the model first.")

# Function to Extract Features from a URL
def extract_features(url):
    parsed_url = urllib.parse.urlparse(url)
    return [
        len(url),  
        url.count('.'),  
        int("@" in url),  
        int("-" in parsed_url.netloc),  
        int(parsed_url.scheme == "https"),  
        parsed_url.netloc.count('.'),  
        url.count('/'),  
        sum(c.isdigit() for c in url),  
        sum(c in "?&=_$" for c in url)  
    ]

# Initialize Flask API
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({"error": "URL missing"}), 400

    # Extract Features
    features = extract_features(url)
    features_df = pd.DataFrame([features])

    # Make Prediction using Random Forest Model
    prediction = rf_model.predict(features_df)[0]

    return jsonify({
        "url": url,
        "prediction": "Phishing" if prediction == 1 else "Legit"
    })

# Run the Flask App
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
