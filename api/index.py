
from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
from pathlib import Path

app = Flask(__name__)
CORS(app)

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "model" / "solar_model.pkl"

with open(MODEL_PATH, "rb") as file:
    model = pickle.load(file)


@app.route("/api/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        features = pd.DataFrame([{
            "AMBIENT_TEMPERATURE": float(data["ambient_temperature"]),
            "MODULE_TEMPERATURE": float(data["module_temperature"]),
            "IRRADIATION": float(data["irradiation"]),
            "HOUR": int(data["hour"]),
            "MONTH": int(data["month"])
        }])

        prediction = float(model.predict(features)[0])

        return jsonify({"prediction": max(0, prediction)})

    except (KeyError, TypeError, ValueError) as error:
        return jsonify({"error": str(error)}), 400

    except Exception:
        return jsonify({"error": "Prediction failed."}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
