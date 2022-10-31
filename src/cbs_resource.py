# %%
import pymysql
import os
from datetime import datetime
from utils import DTEncoder


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
    @staticmethod
    def get_user_by_key(key):

        sql = "SELECT * FROM ms2_db.users where userid=%s"
        conn = CBSresource._get_connection()
        cur = conn.cursor()
        cur.execute(sql, args=key)
        res = cur.fetchone()
        if res:
            result = {'success': True, 'data': res}
        else:
            result = {'success': False, 'message': 'Not Found', 'data': res}

        return result

    @staticmethod
    def verify_login(email, password):

        sql = "SELECT userid FROM ms2_db.users where email=%s and password=%s"
        conn = CBSresource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=(email, password))
        result = cur.fetchone()
        userId = result['userid'] if result else None

        return userId

    @staticmethod
    def register_user(email, username, password):

        sql = "INSERT INTO ms2_db.users (email, username, password) VALUES (%s, %s, %s);"
        conn = CBSresource._get_connection()
        cur = conn.cursor()
        try:
            res = cur.execute(sql, args=(email, username, password))
            # if register success
            result = {'success': True, 'message': 'Register successfully, continue to log in'}
        except pymysql.Error as e:
            print(e)
            result = {'success': False, 'message': 'This email is already registered, try another one'}
        return result

    @staticmethod
    def get_available_session():

        sql = "SELECT * FROM ms2_db.sessions WHERE endtime > %s"
        conn = CBSresource._get_connection()
        cur = conn.cursor()
        try:
            cur.execute(sql, args=(datetime.now()))
            # if register success
            res = cur.fetchall()
            if res:
                result = {'success': True, 'data': res}
            else:
                result = {'success': False, 'message': 'Not Found', 'data': res}
        except pymysql.Error as e:
            print(e)
            result = {'success': False, 'message': str(e)}
        return result

    @staticmethod
    def get_session_by_key(sessionid):

        sql = "SELECT * FROM ms2_db.sessions WHERE sessionid = %s"
        conn = CBSresource._get_connection()
        cur = conn.cursor()
        try:
            cur.execute(sql, args=(sessionid))
            # if register success
            res = cur.fetchone()
            if res:
                result = {'success': True, 'data': res}
            else:
                result = {'success': False, 'message': 'Not Found', 'data': res}
        except pymysql.Error as e:
            print(e)
            result = {'success': False, 'message': str(e)}
        return result

    @staticmethod
    def enroll_session(sessionid, userid):
        sql = "INSERT INTO ms2_db.waitlist (sessionid, userid) VALUES (%s, %s)"
        conn = CBSresource._get_connection()
        cur = conn.cursor()
        try:
            cur.execute(sql, args=(sessionid, userid))
            # if register success
            result = {'success': True, 'message': 'You have joined the waitlist'}

        except pymysql.Error as e:
            print(e)
            res = 'ERROR'
            result = {'success': False, 'message': str(e)}
        return result

    @staticmethod
    def quit_waitlist(sessionid, userid):
        sql_p = "SELECT * FROM ms2_db.waitlist WHERE userid = %s AND sessionid = %s;"
        sql = "DELETE FROM ms2_db.waitlist WHERE userid = %s AND sessionid = %s;"
        conn = CBSresource._get_connection()
        cur = conn.cursor()
        try:
            cur.execute(sql_p, args=(sessionid, userid))
            res = cur.fetchone()
            if res:
                cur.execute(sql, args=(sessionid, userid))
                # if register success
                result = {'success': True, 'message': 'You have quitted the waitlist'}
            else:
                result = {'success': False, 'message': 'You are not in the waitlist'}

        except pymysql.Error as e:
            print(e)
            res = 'ERROR'
            result = {'success': False, 'message': str(e)}
        return result
####### Start from here
    @staticmethod
    def show_profile(userid):
        sql = "Select userid, email, username, sex, preference, credits, birthday \
               FROM ms2_db.users WHERE userid = %s ;"
        conn = CBSresource._get_connection()
        cur = conn.cursor()
        try:
            cur.execute(sql, args=userid)
            # if register success
            res = cur.fetchall()
            if res:
                result = {'success': True, 'data': res}
            else:
                result = {'success': False, 'message': 'User_id Not Found', 'data': res}
        except pymysql.Error as e:
            print(e)
            result = {'success': False, 'message': str(e)}
        return result


    @staticmethod
    def show_profile2(userid):
        sql = "Select userid, email, username, sex, preference, credits, \
               year(birthday) as year, month(birthday) as month, day(birthday) as day \
               FROM ms2_db.users WHERE userid = %s ;"
        conn = CBSresource._get_connection()
        cur = conn.cursor()
        try:
            cur.execute(sql, args=userid)
            # if register success
            res = cur.fetchall()
            if res:
                result = {'success': True, 'data': res}
            else:
                result = {'success': False, 'message': 'User_id Not Found', 'data': res}
        except pymysql.Error as e:
            print(e)
            result = {'success': False, 'message': str(e)}
        return result

    @staticmethod
    def edit_profile(username, sex, preference, email, userid):
        sql_p = "SELECT preference FROM ms2_db.users WHERE userid = %s;"
        sql = "UPDATE ms2_db.users \
               SET username=%s, sex= %s, preference=%s, email=%s \
               WHERE userid=%s;"
        ##### need to be editted again...
        conn = CBSresource._get_connection()
        cur = conn.cursor()
        try:
            cur.execute(sql_p, args=(userid))
            res = cur.fetchone()
            if res:
                cur.execute(sql, args=(username, sex,  preference, email, userid))
                # if register success
                result = {'success': True, 'message': 'You have successfully edited the profile'}
            else:
                result = {'success': False, 'message': 'You fail to edit the profile'}

        except pymysql.Error as e:
            print(e)
            res = 'ERROR'
            result = {'success': False, 'message': str(e)}
        return result

    @staticmethod
    def reset_password(email, old_password, new_password):
        sql_p = "SELECT userid FROM ms2_db.users WHERE email = %s and password= %s;"
        sql = "UPDATE ms2_db.users \
               SET password=%s \
               WHERE email=%s and password= %s;"
        conn = CBSresource._get_connection()
        cur = conn.cursor()
        try:
            cur.execute(sql_p, args=(email, old_password))
            res = cur.fetchone()
            if res:
                cur.execute(sql, args=(new_password, email, old_password))
                result = {'success': True, 'message': 'Resetting successfully, continue to log in'}
            else:
                result = {'success': False, 'message': 'Forget your password?'}

        except pymysql.Error as e:
            print(e)
            result = {'success': False, 'message': 'Anything wrong with password...'}
        return result

    def add_partner(userid_from, userid_to):
        sql_p = "SELECT * FROM ms2_db.partners WHERE userid_from=%s and userid_to=%s ;"
        ## check whether have another partner
        sql_q = "SELECT * FROM ms2_db.users WHERE userid=%s ;"
        ## check whether there is a guy who is in the user's table.
        sql = "INSERT INTO ms2_db.partners (userid_from, userid_to) VALUES (%s, %s)"
        conn = CBSresource._get_connection()
        cur = conn.cursor()
        try:
            cur.execute(sql_p, args=(userid_from, userid_to))
            res1 = cur.fetchone()
            cur.execute(sql_p, args=(userid_to, userid_from))
            res2 = cur.fetchone()
            cur.execute(sql_q, args=(userid_to))
            res3 = cur.fetchone()
            cur.execute(sql_q, args=(userid_from))
            res4 = cur.fetchone()
            if (not res1) and (not res2) and int(userid_from) != int(userid_to) and res3 and res4 :
                cur.execute(sql, args=(userid_from, userid_to))
                result = {'success': True, 'message': 'add the partner successfully!'}
            else:
                result = {'success': False, 'message': 'Sorry, this one already has another partner'}
            ## consideration includes: cannot add itself, cannot add people beyond user's id, cannot add people haing pa
        except pymysql.Error as e:
            print(e)
            result = {'success': False, 'message': '...epic wrong!'}
        return result

    def delete_partner(userid_from, userid_to):
        sql_p = "SELECT * FROM ms2_db.partners WHERE userid_from=%s and userid_to=%s;"
        sql = "DELETE FROM  Ms2_db.partners WHERE userid_from=%s and userid_to=%s;"
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
               FROM ms2_db.partners WHERE userid_to = %s ;"
        sql_q = "Select userid_to\
               FROM ms2_db.partners WHERE  userid_from= %s ;"
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


## Chatting
    def get_chatting_history(userid_from, userid_to):
            sql = "Select * \
                   FROM ms2_db.chatting_form WHERE userid_from = %s and userid_to = %s \
                   UNION\
                   Select * \
                   FROM ms2_db.chatting_form WHERE userid_from = %s and userid_to = %s ;"
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

        sql_q = "SELECT * FROM ms2_db.users WHERE userid=%s;"
        sql = "INSERT INTO ms2_db.chatting_form (userid_from, userid_to,content,time) \
               VALUES (%s, %s,%s, %s);"
        conn = CBSresource._get_connection()
        cur = conn.cursor()
        try:
            cur.execute(sql_q, args=(userid_to))
            res3 = cur.fetchone()
            cur.execute(sql_q, args=(userid_from))
            res4 = cur.fetchone()
            if int(userid_from) != int(userid_to) and res3 and res4:
                cur.execute(sql, args=(userid_from, userid_to,content,datetime.now()))
                result = {'success': True, 'message': 'send it successfully!'}
            else:
                result = {'success': False, 'message': 'Sorry, something wrong'}
            ## consideration includes: cannot add itself, cannot add people beyond user's id
        except pymysql.Error as e:
            print(e)
            result = {'success': False, 'message': '...epic wrong!'}
        return result



# %%
