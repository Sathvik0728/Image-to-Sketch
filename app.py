from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session
)

import cv2
import numpy as np
import base64

app = Flask(__name__)

# Secret key for session
app.secret_key = "sketch_secret_key"

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

    # ==========================================
    # HANDLE IMAGE UPLOAD
    # ==========================================

    if request.method == "POST":

        file = request.files.get("photo")

        if file:

            # Read image
            file_bytes = np.frombuffer(
                file.read(),
                np.uint8
            )

            image = cv2.imdecode(
                file_bytes,
                cv2.IMREAD_COLOR
            )

            # Resize large image
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

            # Create sketch
            sketch = convert_to_pencil_sketch(image)

            # Encode to base64
            _, buffer = cv2.imencode(
                ".jpg",
                sketch
            )

            sketch_base64 = base64.b64encode(
                buffer
            ).decode("utf-8")

            # Save temporarily in session
            session["sketch_image"] = (
                f"data:image/jpeg;base64,{sketch_base64}"
            )

            # Redirect after POST
            return redirect(url_for("index"))

    # ==========================================
    # GET REQUEST
    # ==========================================

    sketch_image = session.pop(
        "sketch_image",
        None
    )

    return render_template(
        "index.html",
        sketch_image=sketch_image
    )

# ==========================================
# RUN APP
# ==========================================

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000)