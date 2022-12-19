from flask import Flask, Response, request
from datetime import datetime
import json
import os
from cbs_resource import CBSresource
from flask_cors import CORS
from utils import DTEncoder
from sns_new_trial import SNS

# Create the Flask application object.
app = Flask(__name__,
            static_url_path='/',
            static_folder='static/class-ui/',
            template_folder='web/templates')

# CORS(app)
cors = CORS(app, resources={r'/api/*': {'origins': '*'}})


##### Youyuan Kong's file, start from here.

@app.before_request
def before_decorator():
    print('Before request I should do...')
    # Verify it is an admin or a user
    #print(request.form)
    #print(request.values)
    #print(request.url)
    #print(request.url_rule)
    #print(request.data)

@app.after_request
def after_decorator(rsp):
    print('After request I should do...')
    ## make sure the invitation successfully be sent and it is the send_invitation method
    if request.url[-15:] == "send_invitation" and rsp.data.decode().__contains__("true"):
        result=CBSresource.ms2_get_profile_1(request.json["userid_to"])
        email=result["data"][0]['email']
        id=result["data"][0]['userid']
        content="You received a partner invitation, please check it on our web: "
        Topic_ARN = f'{os.environ.get("Topic_ARN")}{id}'
        ## Topic_ARN=f'{os.environ.get("Topic_ARN")}{email}'
        ## Topic_ARN = f'{os.environ.get("Topic_ARN")}CBS'
        created =False;
        for each in SNS.list_topics(SNS.sns_client, SNS.logger)['Topics']:
            if(Topic_ARN==each['TopicArn']):
                SNS.sns_client.publish(TopicArn=Topic_ARN,
                                       Message=content,
                                       Subject="Notification from the Badminton Club")
                created = True

        if created == False:
            topic_mame=SNS.create_topic(SNS.sns_client, SNS.logger, str(id))
            response = SNS.subscribe(SNS.sns_client, SNS.logger, Topic_ARN, "email", email)
            print(response)
            ## SNS.sns_client.publish(TopicArn=Topic_ARN,
            ##                       Message=content,
            ##                       Subject="Notification from the Badminton Club")
        else:
            print(1)


    else:
        print("There is nothing I can do!")
        print(request.url[-15:])
    return rsp

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

@app.route("/api/user/<userid>/reject_partner", methods=["POST"])
def reject_invitation(userid):
    if request.method == 'POST':
        user_id_res = CBSresource.reject_invitation(userid, request.get_json()['userid_from'])
        ### response!!!!
        if not user_id_res['success']:
            result = {'success': False, 'message': 'wrong'}
            rsp = Response(json.dumps(result), status=200, content_type="application.json")
        else:
            result = {'success': True, 'message': 'reject someone successfully'}
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

@app.route("/api/user/<userid>/partner/invitation", methods=["GET"])
def get_invitation(userid):
    if request.method == 'GET':

        result = CBSresource.get_invitation2(userid)
        if result['success']:
            rsp = Response(json.dumps(result), status=200, content_type="application.json")
        else:
            rsp = Response(json.dumps(result), status=404, content_type="application.json")
    else:
        rsp = Response("Methods not defined", status=404, content_type="text/plain")
    return rsp


@app.route("/api/user/<userid>/partner/send_invitation", methods=["POST"])
def send_invitation(userid):
    if request.method == 'POST':
        user_id_res = CBSresource.send_invitation(userid, request.get_json()['userid_to'], request.get_json()['content'])
        if not user_id_res['success']:
            result = {'success': False, 'message': 'This Partner cannot be added'}
            rsp = Response(json.dumps(result), status=200, content_type="application.json")
        else:
            result = {'success': True, 'message': 'add the partner successfully'}
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
    app.run(host="0.0.0.0", port=5010, debug=True)
##  app.run(host='127.0.0.1', port=5011, debug=True)
