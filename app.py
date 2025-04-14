import os
import joblib
import urllib.parse
from flask import Flask, request, jsonify

# ✅ Load Random Forest Model
RF_MODEL_PATH = "random_forest_model.pkl"

try:
    rf_model = joblib.load(RF_MODEL_PATH)
except FileNotFoundError:
    raise FileNotFoundError(f"❌ {RF_MODEL_PATH} not found. Train and save the model first.")

# 🚀 Feature Extraction (no pandas)
def extract_features(url):
    parsed_url = urllib.parse.urlparse(url)
    return [[
        len(url),
        url.count('.'),
        int("@" in url),
        int("-" in parsed_url.netloc),
        int(parsed_url.scheme == "https"),
        parsed_url.netloc.count('.'),
        url.count('/'),
        sum(c.isdigit() for c in url),
        sum(c in "?&=_$" for c in url)
    ]]

# 🔥 Flask App
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({"error": "URL missing"}), 400

    features = extract_features(url)
    prediction = rf_model.predict(features)[0]
    
    return jsonify({
        "url": url,
        "prediction": "Phishing" if prediction == 1 else "Legit"
    })

# 🏁 Entry Point
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
