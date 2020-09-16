from web.utils.TokenAuthorize import auth
from flask import Flask, request, jsonify, make_response
from web.static import APIRETURN
from web.static.APIRETURN import add_more_info as add
from utils.database import ResultHandler, SubHandler
import configparser
from web.utils import Register, TokenAuthorize
import json

app = Flask(__name__)

__VERSION__ = "0.0.1"


@app.route('/')
def redirect():
    return "<p>still in progress</p>"


@app.route('/api/v1/results', methods=["POST"])
def task_handler():
    if not request.form.get("token"):
        return make_response(APIRETURN.EMPTY, 200)

    token = request.form.get("token")

    if TokenAuthorize.auth(token):
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
            return make_response(APIRETURN.EMPTY_ARGS_GUIDE, 400)
        return make_response(result, 200)
    else:
        return make_response(APIRETURN.UNAUTHORIZED, 401)


@app.route("/api/v1/subscriptions", methods=["POST"])
def subscriptions_handler():
    token = request.form.get("token")
    if not token:
        return make_response(jsonify(APIRETURN.EMPTY), 200)

    if not TokenAuthorize.auth(token):
        return make_response(jsonify(APIRETURN.UNAUTHORIZED), 401)

    subs = request.form.get("subs")

    if subs:
        try:
            subs = json.loads(subs)
        except json.decoder.JSONDecodeError:
            return make_response(add(APIRETURN.INVALID, "Expected JSON format style"), 400)
        s = SubHandler.SubHandler()
        for sub in subs:
            if not isinstance(sub, dict):
                return make_response(add(APIRETURN.INVALID, "OBJECT IN LIST MUST BE DICT"), 400)

            name = sub.get("name")
            link = sub.get("link")

            if not (name and link):
                return make_response(add(APIRETURN.INVALID, "CANT NOT INPUT NULL VALUES"), 400)

            result = s.add_new_subscriptions(name, link)

            if not result["ok"]:
                return make_response(APIRETURN.INTERNAL_SERVER_ERROR, 500)
        
        return make_response(add(APIRETURN.OK, "INSERTION DONE"), 200)

    args = request.form.get("search")

    if not args:
        return make_response(add(APIRETURN.EMPTY, "Server expected subs link or search args but get none"), 400)
    
    try:
        args = json.loads(args)
    except json.decoder.JSONDecodeError:
        return make_response(add(APIRETURN.INVALID, "Expected JSON format style"), 400)

    if not isinstance(args, list):
        return make_response(add(APIRETURN.INVALID, "SEARCH MUST BE A LIST"), 400)

    s = SubHandler.SubHandler()
    results = []
    for arg in args:
        response = s.get_sub_link_by_name(arg)
        if response:
            results.append(response)

    return make_response(jsonify(ok=True, results=results), 200)


@app.route("/api/v1/verification", methods=["POST"])
def verify():
    parser = configparser.ConfigParser()
    parser.read("web/config/settings.ini")
    StartUpToken = parser.get("Privacy", "StartUpToken")
    if StartUpToken != "0":
        token = request.form.get("token")
        if not token:
            return make_response(
                add(APIRETURN.EMPTY, "Verification need a token but get none"), 400)
        if token != StartUpToken:
            return make_response(add(APIRETURN.UNAUTHORIZED, "Unexpected token"), 401)

        name = request.form.get("name")
        uid = request.form.get("uid")
        permission = "admin"
        if not (name and uid):
            return make_response(add(APIRETURN.INVALID, "Missing arguments"), 400)

        result = Register.register(name, uid, permission)

        if result["ok"]:
            parser.set("Privacy", "StartUpToken", "0")
            parser.write(open("web/config/settings.ini", "w"))

        return make_response(jsonify(result), 200)

    return make_response(add(APIRETURN.NOTFOUND, "This page has been removed."), 404)


@app.route("/api/v1/users", methods=["POST"])
def handle_users():
    return make_response()


@app.errorhandler(404)
def not_fount(error):
    return make_response(jsonify(APIRETURN.NOTFOUND), 404)

@app.errorhandler(405)
def error_method(error):
    return make_response(jsonify(ok=False, descriptions="This method is not allow"), 405)

if __name__ == '__main__':
    app.run(debug=True)
