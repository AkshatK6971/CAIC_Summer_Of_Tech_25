from flask import Flask, request, jsonify
import joblib
import numpy as np
import math
from textblob import TextBlob
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load model and label encoders
model = joblib.load('like_predictor.pkl')
le_company = joblib.load('le_company.pkl')
le_username = joblib.load('le_username.pkl')
le_day = joblib.load('le_day.pkl')

def safe_label_transform(le, value):
    if value in le.classes_:
        return le.transform([value])[0]
    else:
        return -1

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    # Extract required fields
    has_media = int(data.get('has_media', 0))
    content = data.get('content', "")
    hour = int(data.get('hour', 12))
    day = data.get('day')
    username = data.get('username')
    company = data.get('company')

    # Calculate derived features
    word_count = len(content.split())
    char_count = len(content)
    sentiment = TextBlob(content).sentiment.polarity

    # Encode categorical variables
    company_encoded = safe_label_transform(le_company, company)
    username_encoded = safe_label_transform(le_username, username)
    day_encoded = safe_label_transform(le_day, day)

    # Prepare features for prediction
    features = np.array([
        has_media,
        hour,
        word_count,
        char_count,
        sentiment,
        company_encoded,
        username_encoded,
        day_encoded
    ]).reshape(1, -1)

    # Predict log-likes and exponentiate
    log_likes = model.predict(features)[0]
    predicted_likes = int(round(math.exp(log_likes)))

    return jsonify({'predicted_likes': predicted_likes})

if __name__ == '__main__':
    app.run(debug=True, port=5000)