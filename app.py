from flask import Flask, request, jsonify
from engine.master_engine import measure
import os

app = Flask(__name__)

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