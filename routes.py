from flask import Flask, send_from_directory
import os

app = Flask(
    __name__,
    static_url_path="/static",
    static_folder=os.path.join(os.getcwd(), "static"),
)


@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/images/<filename>")
def send_image(filename):
    return send_from_directory("images", filename)


@app.route("/output_img/<filename>")
def output_image(filename):
    return send_from_directory("output_img", filename)


@app.route("/static/<path:filename>")
def custom_static(filename):
    return send_from_directory(os.path.join(os.getcwd(), "./static"), filename)


@app.route("/assets/<path:filename>")
def custom_assets(filename):
    return send_from_directory(os.path.join(os.getcwd(), "./assets"), filename)
