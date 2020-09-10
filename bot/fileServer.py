# -*- coding: utf-8 -*-
# author: Avimitin
# datetime: 2020/9/10 15:24
from flask import Flask, request, make_response, jsonify
from werkzeug.utils import secure_filename
from bot.BotInstance import BOT, ADMIN

app = Flask(__name__)
__TOKEN__ = "dev"


@app.route("/upload", methods=["POST"])
def get_file():
    if "token" not in request.json or request.json["token"] != __TOKEN__:
        return make_response(
            jsonify(ok=False, error_code=401, descriptions="Invalid token"),
            401
        )

    try:
        files = request.files["test_file"]

        if files.filename == "":
            return make_response(
                jsonify(ok=False, error_code=400, descriptions="No file selected"),
                400
            )

        if files and _is_illegal_file(files.filename):
            BOT.send_photo(ADMIN, files)
            return make_response(
                jsonify(ok=True)
            )
    except KeyError:
        return make_response(
            jsonify(ok=False, error_code=400, descriptions="No file received"),
            400
        )


def _is_illegal_file(fileName: str):
    return "." in fileName and fileName.split(".")[1].lower() in ["jpg", "png"]


if __name__ == '__main__':
    app.run(debug=True)
