from flask import Flask, request, jsonify
from engine.master_engine import measure
from flask_cors import CORS   #for CORS
import os

app = Flask(__name__)
#CORS(app)

CORS(
    app,
    origins=[
        "http://localhost:5173",
        "http://localhost",
        "https://localhost",
    ]
)

@app.route("/measure", methods=["POST"])
def measure_api():
    image = request.files["image"]
    height = float(request.form["height"])
    garment = request.form["garment"]
    fit = request.form.get("fit")

    path = "temp.jpg"
    image.save(path)

    result = measure(path, height, garment, fit)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)


# python app.py
