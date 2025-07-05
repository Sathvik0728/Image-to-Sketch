# Pencil Sketch Web App

## Overview
This is a Flask-based web application that allows users to upload an image and convert it into a pencil sketch using OpenCV. The app provides a simple interface for uploading images and displaying the generated sketch.

## Features
- Upload an image via a web form.
- Convert the uploaded image to a pencil sketch using OpenCV.
- Display the generated sketch on the webpage.
- Automatically save uploaded images and sketches in the `static/sketches` directory.

## Prerequisites
- Python 3.6+
- Flask
- OpenCV (`cv2`)
- Werkzeug

## Installation
1. Clone the repository or download the source code.
2. Install the required Python packages:
   ```bash
   pip install flask opencv-python werkzeug
   ```
3. Ensure the `static/sketches` directory is created (it will be created automatically on the first run).

## Usage
1. Run the Flask application:
   ```bash
   python app.py
   ```
2. Open a web browser and navigate to `http://127.0.0.1:5000/`.
3. Upload an image using the file input and click "Generate Sketch".
4. The generated pencil sketch will be displayed on the page.

## File Structure
- `app.py`: The main Flask application with image processing logic.
- `templates/index.html`: The HTML template for the web interface.
- `static/sketches/`: Directory where uploaded images and generated sketches are stored.

## How It Works
- The app uses Flask to handle HTTP requests and serve the web interface.
- Uploaded images are saved to the `static/sketches` directory.
- OpenCV processes the image to create a pencil sketch effect using grayscale conversion, histogram equalization, and Gaussian blur.
- The generated sketch is saved and displayed on the webpage.

## Notes
- Ensure the uploaded image is in a compatible format (e.g., JPG, PNG).
- The app runs in debug mode by default (`app.run(debug=True)`). Disable debug mode in production.
- The sketch generation parameters (e.g., Gaussian blur kernel size, scale) can be adjusted in the `convert_to_pencil_sketch` function for different effects.

## Troubleshooting
- If the sketch fails to generate, check the console for error messages (e.g., invalid image path or format).
- Ensure the `static/sketches` directory has write permissions.
- Verify that all required Python packages are installed.

## License
This project is licensed under the MIT License.
