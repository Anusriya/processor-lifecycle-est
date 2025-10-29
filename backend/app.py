from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import pandas as pd
import joblib
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Load models
kmeans = joblib.load("kmeans_model.joblib")
scaler = joblib.load("scaler.joblib")
label_mapping = joblib.load("label_mapping.joblib")

# Connect to MongoDB
import os

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/recore_db")
client = MongoClient(MONGO_URI)

db = client.get_database()  # auto uses DB from URI

collection = db["classified_results"]


@app.route('/predict', methods=['POST'])
def predict():
    try:
        file = request.files['file']
        df = pd.read_csv(file)

        # Preprocessing
        scaled_data = scaler.transform(df.values)
        cluster_labels = kmeans.predict(scaled_data)
        class_labels = [label_mapping[label] for label in cluster_labels]

        df['Predicted_Class'] = class_labels

        # ✅ Assign batch ID for this upload
        batch_id = datetime.utcnow().isoformat()
        df["batch_id"] = batch_id

        # Save to MongoDB
        records = df.to_dict(orient="records")
        collection.insert_many(records)

        return jsonify({
            "message": "success",
            "total_records": len(records),
            "batch_id": batch_id   # ✅ return batch id to frontend if needed
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/', methods=['GET'])
def home():
    return "Backend Running", 200


if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5000)

