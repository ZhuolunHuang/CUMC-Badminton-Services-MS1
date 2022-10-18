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

        # set by environment variables
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


        
        



# %%
