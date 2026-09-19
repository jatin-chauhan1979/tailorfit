from flask import Flask, request, jsonify
from measurements import get_measurements
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/measure", methods=["POST"])
def measure():
    file = request.files["image"]
    height = float(request.form.get("height", 170))
    garment = request.form.get("garment", "shirt").lower()
    fit = request.form.get("fit", "regular").lower()

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    data = get_measurements(path, height, garment,fit)

    if not data:
        return jsonify({"error": "Body not detected"}), 400

    #return jsonify(data)
    return jsonify({
        "garment": garment,
        "fit": fit,
        "measurements": data
    })

if __name__ == "__main__":
    app.run(debug=True)
