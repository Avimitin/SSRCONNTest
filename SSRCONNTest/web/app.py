from flask import Flask, request, jsonify, make_response
from web.static import APIRETURN
from utils.database import ResultHandler, SubHandler, UserHandler
from utils.TokenGenerator import Generator
import configparser
from web.utils import Register, TokenAuthorize

app = Flask(__name__)

__TOKEN__ = "dev"

__VERSION__ = "0.0.1"


@app.route('/')
def redirect():
    return "<p>still in progress</p>"


@app.route('/api/v1/results', methods=["POST"])
def task_handler():
    if request.json is None or "token" not in request.json:
        return make_response(jsonify(APIRETURN.EMPTY), 200)

    if request.json["token"] == __TOKEN__:
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
    else:
        return make_response(jsonify(APIRETURN.UNAUTHORIZED), 401)


@app.route("/api/v1/subscriptions", methods=["POST"])
def subscriptions_handler():
    if request.form is None or "token" not in request.form:
        return make_response(jsonify(APIRETURN.EMPTY), 200)

    if request.form["token"] == __TOKEN__:
        try:
            subs = request.form["subs"]
            if not subs:
                return make_response(
                    APIRETURN.add_more_info(
                        APIRETURN.EMPTY,
                        "YOU MUST ADD SOME SUB INFO IN THE LIST"
                    ),
                    200
                )

            for sub in subs:
                if not isinstance(sub, dict):
                    return make_response(
                        APIRETURN.add_more_info(APIRETURN.INVALID, "OBJECT IN LIST MUST BE DICT"), 
                        400)
                
                if "name" not in sub.keys() and "link" not in sub.keys():
                    return make_response(
                        APIRETURN.add_more_info(APIRETURN.INVALID, "UNKNOWN KEY, NEED ARGS LIKE THIS: "
                                                                    "{'name': 'name', 'link': 'link'}"),
                        400
                    )
                if sub["name"] is None or sub["link"] is None:
                    return make_response(
                        APIRETURN.add_more_info(APIRETURN.INVALID, "CANT NOT INPUT NULL VALUES"), 400)
                
                s = SubHandler.SubHandler()
                result = s.add_new_subscriptions(sub["name"], sub["link"])
                
                if result["ok"]:
                    return make_response(APIRETURN.add_more_info(APIRETURN.OK, "INSERTION DONE"), 200)
                
                return make_response(APIRETURN.INTERNAL_SERVER_ERROR, 500)

        except KeyError:
            if not request.form.get("search"):
                return make_response(
                    jsonify(APIRETURN.add_more_info(APIRETURN.INVALID, "PUT SUBS OR SEARCH INTO YOUR POST FILE")), 400)

            args = request.form.get("search")
            if not isinstance(args, list):
                return make_response(
                        jsonify(APIRETURN.add_more_info(APIRETURN.INVALID, "SEARCH MUST BE A LIST"), 400))

            s = SubHandler.SubHandler()
            results = []
            for arg in args:
                response = s.get_sub_link_by_name(arg)
                if response:
                    results.append(response)

            return make_response(jsonify(ok=True, results=results), 200)

        except IndexError:
            return make_response(
                    APIRETURN.add_more_info(
                        APIRETURN.INVALID,
                        'Exp: '
                        '{"subs": [{"name": "name", "link": "link"}]}'
                    ),
                400
            )
        except Exception:
            return make_response(jsonify(ok=False, descriptions="Unknow Error Occur", more_info=Exception), 500)
    else:
        return make_response(jsonify(APIRETURN.UNAUTHORIZED), 401)


@app.route("/api/v1/verification", methods=["POST"])
def verify():
    parser = configparser.ConfigParser()
    parser.read("web/config/settings.ini")
    StartUpToken = parser.get("Privacy", "StartUpToken")
    if StartUpToken != "0":
        token = request.form.get("token")
        if not token:
            return make_response(
                jsonify(APIRETURN.add_more_info(APIRETURN.EMPTY, "First time verify need a StartUpToken")),
                400
            )
        if token != StartUpToken:
            return make_response(
                jsonify(APIRETURN.add_more_info(APIRETURN.UNAUTHORIZED, "Unexpected token")),
                401)

        name = request.form.get("name")
        uid = request.form.get("uid")
        permission = "admin"
        if not (name and uid):
            return make_response(
                jsonify(APIRETURN.add_more_info(APIRETURN.INVALID, "Missing arguments")),
                400
            )
        g = Generator.TokenGenerator()
        salt, token = g.new(name, uid)

        u = UserHandler.UserHandler()
        result = u.add_users(uid, name, permission, token)

        if result["ok"]:
            parser.set("Privacy", "StartUpToken", "0")
            parser.write(open("web/config/settings.ini", "w"))

        return make_response(jsonify(result), 200)

    return make_response(APIRETURN.add_more_info(APIRETURN.NOTFOUND, "This page has been removed."), 404)


@app.route("/api/v1/users")
def handle_users():
    return make_response()

@app.errorhandler(404)
def not_fount(error):
    return make_response(jsonify(APIRETURN.NOTFOUND), 404)



if __name__ == '__main__':
    app.run(debug=True)
