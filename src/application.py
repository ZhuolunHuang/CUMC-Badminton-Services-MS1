from flask import Flask, Response, request
from datetime import datetime
import json
from cbs_resource import CBSresource
from flask_cors import CORS
from utils import DTEncoder

# Create the Flask application object.
app = Flask(__name__,
            static_url_path='/',
            static_folder='static/class-ui/',
            template_folder='web/templates')

# CORS(app)
cors = CORS(app, resources={r'/api/*': {'origins': '*'}})


@app.route("/api/user/login", methods=["POST"])
def login():
    if request.method == 'POST':
        user_id_res = CBSresource.verify_login(request.get_json()['email'], request.get_json()['password'])
        if user_id_res:
            result = {'success': True, 'message': 'login successful', 'userId': user_id_res}
            rsp = Response(json.dumps(result), status=200, content_type="application.json")
        else:
            result = {'success': False, 'message': 'Wrong username or password'}
            rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("Methods not defined", status=404, content_type="text/plain")
    return rsp


@app.route("/api/user/register", methods=["POST"])
def register():
    if request.method == 'POST':
        result = CBSresource.register_user(request.get_json()['email'], request.get_json()['username'],
                                           request.get_json()['password'])
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("Methods not defined", status=404, content_type="text/plain")
    return rsp


@app.route("/api/session", methods=["GET"])
def get_available_session():
    result = CBSresource.get_available_session()
    if result['success']:
        rsp = Response(json.dumps(result, cls=DTEncoder), status=200, content_type="application.json")
    else:
        rsp = Response(json.dumps(result, cls=DTEncoder), status=404, content_type="application.json")
    return rsp


@app.route("/api/session/<sessionid>", methods=["GET"])
def get_session_by_key(sessionid):
    result = CBSresource.get_session_by_key(sessionid)
    if result['success']:
        rsp = Response(json.dumps(result, cls=DTEncoder), status=200, content_type="application.json")
    else:
        rsp = Response(json.dumps(result, cls=DTEncoder), status=404, content_type="application.json")
    return rsp


@app.route("/api/session/<sessionid>/enroll/<userid>", methods=["GET"])
def enroll_session(sessionid, userid):
    result = CBSresource.enroll_session(sessionid, userid)
    if result['success']:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response(json.dumps(result), status=404, content_type="application.json")
    return rsp


@app.route("/api/session/<sessionid>/quit/<userid>", methods=["GET"])
def quit_waitlist(sessionid, userid):
    result = CBSresource.quit_waitlist(sessionid, userid)
    if result['success']:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response(json.dumps(result), status=404, content_type="application.json")
    return rsp


##### Youyuan Kong's file, start from here.

@app.route("/api/userprofile/<userid>", methods=["GET"])
def show(userid):
    result = CBSresource.show_profile(userid)
    if result['success']:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response(json.dumps(result), status=404, content_type="application.json")
    return rsp


@app.route("/api/userprofile/edit/<userid>", methods=["POST"])
def edit(userid):
    ## where post id is important
    if request.method == 'POST':
        result = CBSresource.edit_profile(request.get_json()['username'], request.get_json()['sex'],
                                          request.get_json()['birthday'], request.get_json()['preference'],
                                          request.get_json()['credits'], userid)
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("Methods not defined", status=404, content_type="text/plain")
    return rsp


@app.route("/api/user/reset", methods=["POST"])
def reset():
    if request.method == 'POST':
        user_id_res = CBSresource.reset_password(request.get_json()['email'], request.get_json()['old_password'],
                                                 request.get_json()['new_password'])
        if user_id_res:
            result = {'success': True, 'message': 'changing successful'}
            rsp = Response(json.dumps(result), status=200, content_type="application.json")
        else:
            result = {'success': False, 'message': 'Wrong username or password'}
            rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("Methods not defined", status=404, content_type="text/plain")
    return rsp


@app.route("/api/user/<userid>/add_partner", methods=["POST"])
def add_partner(userid):
    if request.method == 'POST':
        user_id_res = CBSresource.add_partner(userid, request.get_json()['userid_to'])
        ### response!!!!
        if not user_id_res['success']:
            result = {'success': False, 'message': 'This Partner cannot be added'}
            rsp = Response(json.dumps(result), status=200, content_type="application.json")
        else:
            result = {'success': True, 'message': 'add the partner successfully'}
            rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("Methods not defined", status=404, content_type="text/plain")
    return rsp


@app.route("/api/user/<userid>/delete_partner", methods=["POST"])
def delete_partner(userid):
    if request.method == 'POST':
        user_id_res = CBSresource.delete_partner(userid, request.get_json()['userid_to'])
        if not user_id_res['success']:
            result = {'success': False, 'message': 'No Partners cannot be deleted'}
            rsp = Response(json.dumps(result), status=200, content_type="application.json")
        else:
            result = {'success': True, 'message': 'delete the partner successfully'}
            rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("Methods not defined", status=404, content_type="text/plain")
    return rsp


@app.route("/api/user/<userid>/chatting/history", methods=["POST"])
def get_chatting_history(userid):
    result = CBSresource.get_chatting_history(userid, request.get_json()['userid_to'])
    if result['success']:
        rsp = Response(json.dumps(result, cls=DTEncoder), status=200, content_type="application.json")
    else:
        rsp = Response(json.dumps(result, cls=DTEncoder), status=404, content_type="application.json")
    return rsp


@app.route("/api/user/<userid>/chatting/sending", methods=["POST"])
def let_us_chat(userid):
    if request.method == 'POST':
        sent = CBSresource.set_chatting(userid, request.get_json()['userid_to'], request.get_json()['content'])
        if not sent['success']:
            result = {'success': False, 'message': 'sending it to the universe'}
            rsp = Response(json.dumps(result), status=404, content_type="application.json")
        else:
            result = {'success': True, 'message': 'sent it successfully!'}
            rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("Methods not defined", status=404, content_type="text/plain")
    return rsp


if __name__ == "__main__":
    app.run(host="localhost", port=5010, debug=True)
