from flask import Flask, request, jsonify, send_file
from html2image import Html2Image
import os

app = Flask(__name__)
hti = Html2Image(custom_flags=["--no-sandbox"])

# Fixed filename for the screenshot
fixed_filename = "screenshot.png"


@app.route("/screenshot", methods=["POST"])
def generate_screenshot():
    try:
        html = request.form["html"]
        css = request.form["css"]

        # Generate screenshot and save it to the current folder
        paths = hti.screenshot(html_str=html, css_str=css, save_as=fixed_filename)

        absolute_path = os.path.abspath(fixed_filename)

        # Send the image file directly
        return send_file(absolute_path, mimetype="image/png")
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
