from flask import Flask, request, jsonify, send_file
import uuid
from html2image import Html2Image
import os

app = Flask(__name__)
hti = Html2Image(custom_flags=["--no-sandbox", "--disable-gpu"], size=(1080, 1080))

# Create the 'images' folder if it doesn't exist
images_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
if not os.path.exists(images_folder):
    os.makedirs(images_folder)


@app.route("/screenshot", methods=["POST"])
def generate_screenshot():
    try:
        html = request.form["html"]
        css = request.form["css"]

        # Generate a random filename using UUID
        random_filename = str(uuid.uuid4()) + ".png"
        absolute_path = os.path.join(images_folder, random_filename)

        # Set the output path for html2image
        hti.output_path = images_folder

        # Print debugging information
        print(f"Attempting to save file to: {absolute_path}")

        # Generate screenshot and save it to the 'images' folder
        paths = hti.screenshot(html_str=html, css_str=css, save_as=random_filename)

        # Create a download link
        download_link = f"https://h2i-nexuswho.koyeb.app/download/{random_filename}"

        return jsonify({"download_link": download_link})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/download/<filename>")
def download_screenshot(filename):
    return send_file(os.path.join(images_folder, filename), as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
