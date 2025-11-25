from flask import Flask, request, send_file
from rembg import remove, new_session
from io import BytesIO
from PIL import Image

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
    output_bytes = remove(input_bytes, session=new_session("u2netp"))

    img = Image.open(BytesIO(output_bytes)).convert("RGBA")
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    return send_file(buf, mimetype="image/png")
