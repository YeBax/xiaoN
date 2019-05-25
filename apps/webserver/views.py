from flask import Flask, request, abort, jsonify
from flask import make_response
from tools.sign import sign_md5
from language.frame import Frame


app = Flask(__name__)
frame_list = []
frame_dict = {}


@app.route("/createFrame", methods=['POST'])
def create_frame():
    if not request.json or 'user_id' not in request.json or 'create_time' not in request.json or 'sign' not in request.json:
        abort(400)
    user_id = request.json['user_id']
    create_time = request.json['create_time']
    sign = request.json['sign']
    if sign != sign_md5(user_id, create_time):
        abort(403)
    print(frame_list)
    if user_id in frame_list:
        json_data = {"code": 1, "msg": "User has created"}
    else:
        frame_list.append(user_id)
        frame = Frame(user_id, create_time)
        frame_id = frame.get_redis_key()
        json_data = {"code": 0, "msg": "Success", "frame_id": frame_id}
        frame_list.append(user_id)
        frame_dict[frame_id] = frame
    return jsonify(json_data), 200


@app.route("/receive", methods=['POST'])
def receive():
    if not request.json:
        abort(400)
    field_list = ['user_id', 'frame_id', 'update_time', 'requests_words', 'sign']
    for field in field_list:
        if field not in request.json:
            abort(400)

    user_id = request.json['user_id']
    frame_id = request.json['frame_id']
    update_time = request.json['update_time']
    requests_words = request.json['requests_words']
    sign = request.json['sign']
    if sign != sign_md5(user_id, update_time):
        abort(403)

    if frame_id in frame_dict:
        frame = frame_dict[frame_id]
        responses_words = frame.receive_talk(requests_words, update_time)
        json_data = {"code": 0, "msg": "Success", "responses_words": responses_words}
        frame_dict[frame_id] = frame
    else:
        json_data = {"code": 1, "msg": "Frame ID not found"}
    return jsonify(json_data), 200


@app.errorhandler(400)
def not_found(error):
    err_json = {
        "code": 1,
        "msg": "Field error"
    }
    return make_response(jsonify(err_json), 400)


@app.errorhandler(403)
def not_found(error):
    err_json = {
        "code": 1,
        "msg": "Sign error"
    }
    return make_response(jsonify(err_json), 400)


@app.errorhandler(404)
def not_found(error):
    err_json = {
        "code": 1,
        "msg": "Not found"
    }
    return make_response(jsonify(err_json), 404)


def run():
    app.run()
