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


##### Youyuan Kong's file, start from here.

@app.route("/api/userprofile/<userid>", methods=["GET"])
def show(userid):
    result = CBSresource.ms2_get_profile_1(userid)
    # result = CBSresource.show_profile(userid)
    if result:
        rsp = Response(json.dumps(result, default=str), status=200, content_type="application.json")
    else:
        rsp = Response(json.dumps(result, default=str), status=404, content_type="application.json")
    return rsp

@app.route("/api/userprofile2/<userid>", methods=["GET"])
def show2(userid):
    result = CBSresource.ms2_get_profile_2(userid)
    # result = CBSresource.show_profile(userid)
    if result:
        rsp = Response(json.dumps(result, default=str), status=200, content_type="application.json")
    else:
        rsp = Response(json.dumps(result, default=str), status=404, content_type="application.json")
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


@app.route("/api/user/<userid>/delete_partner/<userid_to>", methods=["GET"])
def delete_partner(userid, userid_to):
    if request.method == 'GET':
        user_id_res = CBSresource.delete_partner(userid, userid_to)
        if not user_id_res['success']:
            result = {'success': False, 'message': 'No Partners cannot be deleted'}
            rsp = Response(json.dumps(result), status=200, content_type="application.json")
        else:
            result = {'success': True, 'message': 'delete the partner successfully'}
            rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("Methods not defined", status=404, content_type="text/plain")
    return rsp


@app.route("/api/user/<userid>/partner", methods=["GET"])
def get_partner(userid):
    if request.method == 'GET':

        result = CBSresource.show_partner(userid)
        if result['success']:
            rsp = Response(json.dumps(result), status=200, content_type="application.json")
        else:
            rsp = Response(json.dumps(result), status=404, content_type="application.json")
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

@app.route("/api/user/<userid>/search_pro", methods=["POST"])
def get_pro(userid):
    result = CBSresource.ms2_get_profile_3(request.get_json())
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
