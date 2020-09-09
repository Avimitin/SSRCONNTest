from flask import Flask, request, jsonify, make_response
from web.static import APIRETURN
from web.bin.database import ResultHandler, SubHandler

app = Flask(__name__)

TOKEN = "dev"


@app.route('/')
def redirect():
    return "<p>still in progress</p>"


@app.route('/api/v1/results', methods=["POST"])
def task_handler():
    if request.json is None or "token" not in request.json:
        return make_response(jsonify(APIRETURN.EMPTY), 200)

    if request.json["token"] == TOKEN:
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
    if request.json is None or "token" not in request.json:
        return make_response(jsonify(APIRETURN.EMPTY), 200)

    if request.json["token"] == TOKEN:
        try:
            subs = request.json["subs"]
            if not subs:
                return make_response(
                    jsonify(APIRETURN.add_more_info(
                        APIRETURN.EMPTY,
                        "YOU MUST ADD SOME SUB INFO IN THE LIST"
                    )),
                    200
                )
            for sub in subs:
                if not isinstance(sub, dict):
                    return make_response(
                        jsonify(APIRETURN.add_more_info(APIRETURN.INVALID, "OBJECT IN LIST MUST BE DICT"), 400))
                try:
                    name = sub["name"]
                    link = sub["link"]
                except KeyError:
                    return make_response(
                        jsonify(APIRETURN.add_more_info(APIRETURN.INVALID, "UNKNOWN KEY, NEED ARGS LIKE THIS: "
                                                                           "{'name': 'name', 'link': 'link'}")),
                        400
                    )
                if name is None or link is None:
                    return make_response(
                        jsonify(APIRETURN.add_more_info(APIRETURN.INVALID, "CANT NOT INPUT NULL VALUES")), 400)
                else:
                    s = SubHandler.SubHandler()
                    result = s.add_new_subscriptions(name, link)
                    if result["ok"]:
                        return make_response(jsonify(APIRETURN.add_more_info(APIRETURN.OK, "INSERT DONE")), 200)
                    return make_response(jsonify(APIRETURN.INTERNAL_SERVER_ERROR), 500)
        except KeyError:
            if not request.json.get("search"):
                return make_response(
                    jsonify(APIRETURN.add_more_info(APIRETURN.INVALID, "PUT SUBS OR SEARCH INTO YOUR POST FILE")), 400)

            args = request.json.get("search")
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
                jsonify(
                    APIRETURN.add_more_info(
                        APIRETURN.INVALID,
                        'Exp: '
                        '{"subs": [{"name": "name", "link": "link"}]}'
                    )),
                400
            )
        except Exception:
            return make_response(jsonify(ok=False, descriptions="Error Occur", more_info=Exception), 400)
    else:
        return make_response(jsonify(APIRETURN.UNAUTHORIZED), 401)


@app.errorhandler(404)
def not_fount(error):
    return make_response(jsonify(APIRETURN.NOTFOUND), 404)


if __name__ == '__main__':
    app.run(debug=True)
