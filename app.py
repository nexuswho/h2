from flask import (
    Flask,
    request,
    jsonify,
    send_file,
    render_template_string,
    send_from_directory,
)
import uuid
from html2image import Html2Image
import os

app = Flask(__name__)
hti = Html2Image(
    custom_flags=["--no-sandbox", "--disable-gpu"],
    size=(1080, 1080),
)

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
        random_filename = str(uuid.uuid4())
        image_filename = f"{random_filename}.png"
        html_filename = f"{random_filename}.html"
        absolute_image_path = os.path.join(images_folder, image_filename)
        absolute_html_path = os.path.join(images_folder, html_filename)

        # Set the output path for html2image
        hti.output_path = images_folder

        # Print debugging information
        print(f"Attempting to save image file to: {absolute_image_path}")

        # Generate screenshot and save it to the 'images' folder
        paths = hti.screenshot(html_str=html, css_str=css, save_as=image_filename)

        # Generate a simple HTML page with the embedded image
        html_page_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <title>Generated Screenshot</title>
        </head>
        <body>
          <img src="{image_filename}" alt="Generated Screenshot">
        </body>
        </html>
        """

        # Save the HTML page
        with open(absolute_html_path, "w") as html_file:
            html_file.write(html_page_content)

        # Create a download link to the HTML page
        download_link = f"https://h2i-calfkicker.koyeb.app/download/{image_filename}"

        return jsonify({"download_link": download_link})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/download/<filename>")
def download_screenshot(filename):
    # If the requested file is an HTML file, serve it as a page
    if filename.endswith(".html"):
        return send_from_directory(images_folder, filename)

    # Otherwise, serve it as an attachment (e.g., image)
    return send_file(os.path.join(images_folder, filename))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
