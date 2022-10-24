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

        usr = os.environ.get("root")  ## change
        pw = os.environ.get("Kevinsekai232323***")   ## change
        h = os.environ.get("localhost")  ## change

        conn = pymysql.connect(
            user='root',   ## change
            password='Kevinsekai232323***',   ## change
            host='localhost',    ## change
            port=3306,    ## change
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
            result = {'success':True, 'data':res}
        else:
            result = {'success':False, 'message':'Not Found','data':res}

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
            result = {'success':True, 'message':'Register successfully, continue to log in'}
        except pymysql.Error as e:
            print(e)
            result = {'success':False, 'message':'This email is already registered, try another one'}
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
                result = {'success':True, 'data':res}
            else:
                result = {'success':False, 'message':'Not Found','data':res}
        except pymysql.Error as e:
            print(e)
            result = {'success':False, 'message':str(e)}
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
                result = {'success':True, 'data':res}
            else:
                result = {'success':False, 'message':'Not Found','data':res}
        except pymysql.Error as e:
            print(e)
            result = {'success':False, 'message':str(e)}
        return result 

    @staticmethod
    def enroll_session(sessionid, userid):
        sql = "INSERT INTO ms2_db.waitlist (sessionid, userid) VALUES (%s, %s)"
        conn = CBSresource._get_connection()
        cur = conn.cursor()
        try:
            cur.execute(sql, args=(sessionid, userid))
            # if register success
            result = {'success':True, 'message':'You have joined the waitlist'}

        except pymysql.Error as e:
            print(e)
            res = 'ERROR'
            result = {'success':False, 'message':str(e)}
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
                result = {'success':True, 'message':'You have quitted the waitlist'}
            else:
                result = {'success':False, 'message':'You are not in the waitlist'}

        except pymysql.Error as e:
            print(e)
            res = 'ERROR'
            result = {'success':False, 'message':str(e)}
        return result

    @staticmethod
    def show_profile(userid):
        sql = "Select userid, email, username, sex, preference, credits, \
               year(birthday) as year, month(birthday) as month, day(birthday) as day \
               FROM ms2_db.users WHERE userid = %s;"
        conn = CBSresource._get_connection()
        cur = conn.cursor()
        try:
            cur.execute(sql, args=userid)
            # if register success
            res = cur.fetchone()
            if res:
                result = {'success':True, 'data':res}
            else:
                result = {'success':False, 'message':'User_id Not Found','data':res,"resa":userid}
        except pymysql.Error as e:
            print(e)
            result = {'success':False, 'message':str(e)}
        return result
    @staticmethod
    def edit_profile(username, sex, birthday, preference, credits, userid):
        sql_p = "SELECT preference,credits FROM ms2_db.users WHERE userid = %s;"
        sql = "UPDATE ms2_db.users \
               SET username=%s, sex= %s, birthday=%s, preference=%s, credits=%s \
               WHERE userid=%s;"
        conn = CBSresource._get_connection()
        cur = conn.cursor()
        try:
            cur.execute(sql_p, args=(userid))
            res = cur.fetchone()
            if res:
                cur.execute(sql, args=(username, sex, birthday, preference, credits, userid))
                # if register success
                result = {'success':True, 'message':'You have quitted the waitlist'}
            else:
                result = {'success':False, 'message':'You are not in the waitlist'}

        except pymysql.Error as e:
            print(e)
            res = 'ERROR'
            result = {'success':False, 'message':str(e)}
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
                result = {'success': True, 'message':'Resetting successfully, continue to log in'}
            else:
                result = {'success': False, 'message': 'Forget your password?'}

        except pymysql.Error as e:
            print(e)
            result = {'success':False, 'message':'Anything wrong with password...'}
        return result
# %%
