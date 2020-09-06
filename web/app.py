from flask import Flask, request, jsonify, make_response
from web.static import APIRETURN
from web.bin.database import ResultHandler

app = Flask(__name__)

TOKEN = "dev"


@app.route('/')
def redirect():
    return "<p>still in progress</p>"


@app.route('/api/v1/results', methods=["POST"])
def task_handler():
    if request.json is None or "token" not in request.json:
        return make_response(jsonify(APIRETURN.EMPTY), 200)
    elif request.json["token"] == TOKEN:
        name = request.args.get("name")
        time = request.args.get("time")
        r = ResultHandler.ResultHandler()
        if name and time:
            result = r.get_result_by_keyword(name=name, time=time)
        elif name:
            result = r.get_result_by_keyword(name=name)
        elif time:
            result = r.get_result_by_keyword(time=time)
        else:
            return make_response(jsonify(APIRETURN.EMPTY_ARGS_GUIDE), 400)
        return make_response(jsonify(result), 200)


@app.errorhandler(404)
def not_fount(error):
    return make_response(jsonify(APIRETURN.NOTFOUND), 404)


if __name__ == '__main__':
    app.run(debug=True)
