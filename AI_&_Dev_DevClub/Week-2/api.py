from flask import Flask, request, jsonify
import joblib
import numpy as np
import math

app = Flask(__name__)

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

    company_encoded = safe_label_transform(le_company, data['company'])
    username_encoded = safe_label_transform(le_username, data['username'])
    day_encoded = safe_label_transform(le_day, data['day'])
        
    features = np.array([
        data['has_media'],
        data['hour'],
        data['word_count'],
        data['char_count'],
        data['sentiment'],
        company_encoded,
        username_encoded,
        day_encoded
    ]).reshape(1, -1)

    log_likes = model.predict(features)[0]
    predicted_likes = int(round(math.exp(log_likes)))

    return jsonify({'predicted_likes': predicted_likes})

if __name__ == '__main__':
    app.run(debug=True)