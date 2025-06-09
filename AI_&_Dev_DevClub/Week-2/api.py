from flask import Flask, request, jsonify
import joblib
import numpy as np
import math

app = Flask(__name__)

# Load the trained RandomForest model
model = joblib.load('like_predictor.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    features = np.array([
        data['has_media'],         # 1 or 0 (likely always 1 from your data)
        data['hour'],              # int: 0–23
        data['word_count'],        # int
        data['char_count'],        # int
        data['sentiment'],         # float: -1 to 1
        data['company_encoded'],   # int
        data['username_encoded'],  # int
        data['day_encoded']        # int: 0–6
    ]).reshape(1, -1)

    log_likes = model.predict(features)[0]
    predicted_likes = int(round(math.exp(log_likes)))

    return jsonify({'predicted_likes': predicted_likes})

if __name__ == '__main__':
    app.run(debug=True)
