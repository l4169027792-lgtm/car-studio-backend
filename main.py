from io import BytesIO

from flask import Flask, request, send_file
from PIL import Image

from image_utils import image_to_bytes, remove_background_from_bytes

app = Flask(__name__)

@app.route("/")
def index():
    return "Car Studio Backend Running"

@app.route("/api/process-image", methods=["POST"])
def process_image():
    if "file" not in request.files:
        return {"error": "no file provided"}, 400

    file = request.files["file"]
    input_bytes = file.read()

    # Remove background
    img = remove_background_from_bytes(input_bytes)
    buf = BytesIO(image_to_bytes(img))
    buf.seek(0)

    return send_file(buf, mimetype="image/png")
