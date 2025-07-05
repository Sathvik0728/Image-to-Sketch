from flask import Flask, render_template, request
import cv2
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'static/sketches'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure sketch folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def convert_to_pencil_sketch(image_path, output_path):
    image = cv2.imread(image_path)

    if image is None:
        print(f"❌ Failed to read image from path: {image_path}")
        return False

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    inverted = cv2.bitwise_not(gray)
    blurred = cv2.GaussianBlur(inverted, (21, 21), 0)
    inverted_blur = cv2.bitwise_not(blurred)
    sketch = cv2.divide(gray, inverted_blur, scale=199.0)

    success = cv2.imwrite(output_path, sketch)
    if success:
        print(f"✅ Sketch saved: {output_path}")
    else:
        print(f"❌ Failed to save sketch to: {output_path}")
    return success

@app.route("/", methods=["GET", "POST"])
def index():
    sketch_filename = None

    if request.method == "POST":
        file = request.files.get("photo")
        if file:
            filename = secure_filename(file.filename)
            base = os.path.splitext(filename)[0]
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            sketch_name = f"sketch_{base}.jpg"
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], sketch_name)

            file.save(input_path)
            print(f"📤 Uploaded image saved to: {input_path}")

            if convert_to_pencil_sketch(input_path, output_path):
                sketch_filename = sketch_name
            else:
                print("❌ Sketch generation failed.")

            print("📁 Sketches folder contains:", os.listdir(app.config['UPLOAD_FOLDER']))

    return render_template("index.html", sketch_image=sketch_filename)

if __name__ == "__main__":
    app.run(debug=True)
