# %%
import pymysql
import os
import requests
import json
from datetime import datetime
from utils import DTEncoder
''

##os.environ["MS2_URL"] = 'http://127.0.0.1:5011/'


class CBSresource:

    def __int__(self):
        self.current_time = datetime.now()

    @staticmethod
    def _get_connection():

        usr = os.environ.get("DBUSER")
        pw = os.environ.get("DBPW")
        h = os.environ.get("DBHOST")

        conn = pymysql.connect(
            user=usr,
            password=pw,
            host=h,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return conn

    ####### Start from here

    @staticmethod
    def ms2_get_profile_1(userid):

        # set by environment variables
        baseURL = os.environ.get("MS2_URL")
        partnerid = None
        res = requests.get(baseURL  + f'api/userprofile/{userid}').json()
        if res['success']:
            data = res['data'][0]
            partnerid = list(data.values())
        ## can retun partnerid
        return res

    def ms2_get_profile_2(userid):

        # set by environment variables
        baseURL = os.environ.get("MS2_URL")
        partnerid = None
        res = requests.get(baseURL  + f'api/userprofile2/{userid}').json()
        if res['success']:
            data = res['data'][0]
            partnerid = list(data.values())
        ## can retun partnerid
        return res


    #### Partners
    def add_partner(userid_from, userid_to):
        baseURL = os.environ.get("MS2_URL")
        sql_p = "SELECT * FROM ms1_db.partners WHERE userid_from=%s and userid_to=%s ;"
        ## check whether have another partner
        ### sql_q = "SELECT * FROM ms2_db.users WHERE userid=%s ;"
        ## check whether there is a guy who is in the user's table.
        sql = "INSERT INTO ms1_db.partners (userid_from, userid_to) VALUES (%s, %s);"
        sql_2 = "UPDATE ms1_db.invitations SET response = TRUE WHERE  userid_to = %s or userid_to = %s ;"
        conn = CBSresource._get_connection()
        cur = conn.cursor()
        try:
            cur.execute(sql_p, args=(userid_from, userid_to))
            res1 = cur.fetchone()
            cur.execute(sql_p, args=(userid_to, userid_from))
            res2 = cur.fetchone()
            res3 = requests.get(baseURL + f'api/check_partner/{userid_to}').json()
            # cur.execute(sql_q, args=(userid_to))
            # res3 = cur.fetchone()
            res4 = requests.get(baseURL + f'api/check_partner/{userid_from}').json()
            # cur.execute(sql_q, args=(userid_from))
            # res4 = cur.fetchone()
            if (not res1) and (not res2) and int(userid_from) != int(userid_to) and res3["success"] and res4["success"]:
                cur.execute(sql, args=(userid_from, userid_to))
                cur.execute(sql_2, args=(userid_from, userid_to))
                result = {'success': True, 'message': 'add the partner successfully!'}
            else:
                result = {'success': False, 'message': 'Sorry, this one already has another partner'}
            ## consideration includes: cannot add itself, cannot add people beyond user's id, cannot add people haing pa
        except pymysql.Error as e:
            print(e)
            result = {'success': False, 'message': '...epic wrong!'}
        print(result)
        return result

    def reject_invitation(userid_from, userid_to):
        sql = "UPDATE ms1_db.invitations SET response = TRUE WHERE userid_from = %s and userid_to = %s  ;"
        conn = CBSresource._get_connection()
        cur = conn.cursor()
        try:
            cur.execute(sql, args=(userid_from, userid_to))
            result = {'success': True, 'message': 'reject someone successfully!'}

        except pymysql.Error as e:
            print(e)
            result = {'success': False, 'message': '...epic wrong!'}
        return result


    def delete_partner(userid_from, userid_to):
        sql_p = "SELECT * FROM ms1_db.partners WHERE userid_from=%s and userid_to=%s;"
        sql = "DELETE FROM  ms1_db.partners WHERE userid_from=%s and userid_to=%s;"
        conn = CBSresource._get_connection()
        cur = conn.cursor()
        try:
            cur.execute(sql_p, args=(userid_from, userid_to))
            res1 = cur.fetchone()
            cur.execute(sql_p, args=(userid_to, userid_from))
            res2 = cur.fetchone()

            if res1:
                cur.execute(sql, args=(userid_from, userid_to))
                result = {'success': True, 'message': 'delete the partner successfully!'}
            elif res2:
                cur.execute(sql, args=(userid_to, userid_from))
                result = {'success': True, 'message': 'delete the partner successfully!'}
            else:
                result = {'success': False, 'message': 'Sorry, you are lonely'}
            ## consideration includes: cannot add itself, cannot add people beyond user's id, cannot add people haing pa
        except pymysql.Error as e:
            print(e)
            result = {'success': False, 'message': '...epic wrong!'}
        return result

    @staticmethod
    def show_partner(userid):
        sql_p = "Select userid_from\
               FROM ms1_db.partners WHERE userid_to = %s ;"
        sql_q = "Select userid_to\
               FROM ms1_db.partners WHERE  userid_from= %s ;"
        conn = CBSresource._get_connection()
        cur = conn.cursor()
        try:
            cur.execute(sql_p, args=userid)
            res1 = cur.fetchall()
            cur.execute(sql_q, args=userid)
            res2 = cur.fetchall()
            if res1:
                result = {'success': True, 'data': res1}
            elif res2:
                result = {'success': True, 'data': res2}
            else:
                result = {'success': False, 'message': 'I am lonely lonely lonely', 'data': res1}
        except pymysql.Error as e:
            print(e)
            result = {'success': False, 'message': str(e)}
        return result

    def ms2_get_profile_3(email):
        # set by environment variables
        baseURL = os.environ.get("MS2_URL")
        res = requests.post(baseURL  + f'/api/searchprofile', json=email).json()
        if res['success']:
            data = res['data']
            caluse = []
            for j in data:
                caluse.append("userid_to=" + str(j["userid"]))
                caluse.append("userid_from=" + str(j["userid"]))
            sql="Select * from ms1_db.partners where "+" or ".join(caluse)
            conn = CBSresource._get_connection()
            cur = conn.cursor()
            try:
                cur.execute(sql)
                res = cur.fetchall()
                print(res)
                data_B=res
                data_C= []
                for i in data:
                    i["partner"] = None
                    for j in data_B:
                        if i["userid"]==j['Userid_from']: i["partner"]=j['Userid_to']
                        elif i["userid"]==j['Userid_to']:  i["partner"]=j['Userid_from']
                    data_C.append(i)
                if data_C:
                    result = {'success': True, 'data': data_C}
                else:
                    result = {'success': False, 'message': 'Message not found', 'data': data_C}
            except pymysql.Error as e:
                print(e)
                result = {'success': False, 'message': str(e)}
        return result
    def get_invitation(userid_to):
            sql="Select * FROM ms1_db.invitations WHERE userid_to=%s and response=FALSE"
            conn = CBSresource._get_connection()
            cur = conn.cursor()
            try:
                cur.execute(sql, args=userid_to)
                # if get it
                res = cur.fetchall()
                if res:
                    result = {'success': True, 'data': res}
                else:
                    result = {'success': False, 'message': 'So sad, no body loves you', 'data': res}
            except pymysql.Error as e:
                print(e)
                result = {'success': False, 'message': str(e)}
            return result

    def send_invitation(userid_from,userid_to,content):
        baseURL = os.environ.get("MS2_URL")
        sql_p = "SELECT * FROM ms1_db.partners WHERE userid_from=%s or userid_to=%s ;"
        ## check whether you have a partner
        ## check whether have another partner
        ## check whether there is a guy who is in the user's table.
        sql = "INSERT INTO ms1_db.invitations (userid_from, userid_to,Content, response) VALUES (%s, %s, %s, FALSE)"
        conn = CBSresource._get_connection()
        cur = conn.cursor()
        try:
            cur.execute(sql_p, args=(userid_from, userid_from))
            res1 = cur.fetchone()
            cur.execute(sql_p, args=(userid_to, userid_to))
            res2 = cur.fetchone()
            res3 = requests.get(baseURL + f'api/check_partner/{userid_from}').json()
            res4 = requests.get(baseURL + f'api/check_partner/{userid_to}').json()
            if res1:
                result = {'success': False, 'message': 'You have the possibility to have two partners!'}
                print(result)
            elif res2:
                result = {'success': False, 'message': 'Error, you cannot add this guy since it already has 1 partner!'}
                print(result)
            elif not res3["success"]:
                result = {'success': False, 'message': 'You are a guy from universe!'}
                print(result)
            elif not res4["success"]:
                result = {'success': False, 'message': 'The guy you want to find is from universe!'}
                print(result)
            elif userid_from==userid_to:
                result = {'success': False, 'message': 'You wanna interpartner yourself'}
                print(result)
            else:
                cur.execute(sql, args=(userid_from, userid_to, content))
                result = {'success': True, 'message': 'send the inviting request successfully!'}
            ## consideration includes: cannot add itself, cannot add people beyond user's id, cannot add people haing pa
        except pymysql.Error as e:
            print(e)
            result = {'success': False, 'message': '...epic wrong!'}
        return result



## Chatting
    def get_chatting_history(userid_from, userid_to):
            sql = "Select * \
                   FROM ms1_db.chatting_form WHERE userid_from = %s and userid_to = %s \
                   UNION\
                   Select * \
                   FROM ms1_db.chatting_form WHERE userid_from = %s and userid_to = %s ;"
            conn = CBSresource._get_connection()
            cur = conn.cursor()
            try:
                cur.execute(sql, args=(userid_from, userid_to, userid_to, userid_from))
                # if get it
                res = cur.fetchall()
                if res:
                    result = {'success': True, 'data': res}
                else:
                    result = {'success': False, 'message': 'Message not found', 'data': res}
            except pymysql.Error as e:
                print(e)
                result = {'success': False, 'message': str(e)}
            return result

    def set_chatting(userid_from, userid_to, content):
        baseURL = os.environ.get("MS2_URL")
        # sql_q = "SELECT * FROM ms2_db.users WHERE userid=%s;"
        sql = "INSERT INTO ms1_db.chatting_form (userid_from, userid_to,content,time) \
               VALUES (%s, %s,%s, %s);"
        conn = CBSresource._get_connection()
        cur = conn.cursor()
        try:
            # cur.execute(sql_q, args=(userid_to))
            # res3 = cur.fetchone()
            res3 = requests.get(baseURL + f'api/check_partner/{userid_to}').json()
            res4 = requests.get(baseURL + f'api/check_partner/{userid_from}').json()
            # cur.execute(sql_q, args=(userid_from))
            #res4 = cur.fetchone()
            if int(userid_from) != int(userid_to) and res3["success"] and res4["success"]:
                cur.execute(sql, args=(userid_from, userid_to, content, datetime.now()))
                result = {'success': True, 'message': 'send it successfully!'}
            else:
                result = {'success': False, 'message': 'Sorry, something wrong'}
            ## consideration includes: cannot add itself, cannot add people beyond user's id
        except pymysql.Error as e:
            print(e)
            result = {'success': False, 'message': '...epic wrong!'}
        return result



# %%
