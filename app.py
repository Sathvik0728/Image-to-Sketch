from flask import Flask, render_template, request, session, redirect, url_for
import cv2
import numpy as np
import base64
import os

app = Flask(__name__)

app.secret_key = "secret_key"

# ==========================================
# PENCIL SKETCH FUNCTION
# ==========================================

def convert_to_pencil_sketch(image):

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    gray = cv2.equalizeHist(gray)

    inverted = cv2.bitwise_not(gray)

    blurred = cv2.GaussianBlur(
        inverted,
        (21, 21),
        0
    )

    inverted_blur = cv2.bitwise_not(blurred)

    sketch = cv2.divide(
        gray,
        inverted_blur,
        scale=199.0
    )

    return sketch

# ==========================================
# HOME ROUTE
# ==========================================

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        file = request.files.get("photo")

        if file:

            # Read uploaded image
            file_bytes = np.frombuffer(
                file.read(),
                np.uint8
            )

            image = cv2.imdecode(
                file_bytes,
                cv2.IMREAD_COLOR
            )

            if image is None:

                return "Image upload failed"

            # Resize image
            h, w = image.shape[:2]

            max_width = 1000

            if w > max_width:

                ratio = max_width / w

                image = cv2.resize(
                    image,
                    (
                        int(w * ratio),
                        int(h * ratio)
                    )
                )

            # Convert to sketch
            sketch = convert_to_pencil_sketch(image)

            # Encode image
            _, buffer = cv2.imencode(
                ".jpg",
                sketch
            )

            sketch_base64 = base64.b64encode(
                buffer
            ).decode("utf-8")

            session["sketch_image"] = (
                f"data:image/jpeg;base64,{sketch_base64}"
            )

            return redirect(url_for("index"))

    sketch_image = session.pop(
        "sketch_image",
        None
    )

    return render_template(
        "index.html",
        sketch_image=sketch_image
    )

# ==========================================
# RENDER DEPLOYMENT
# ==========================================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )