import pymysql
import os
from datetime import datetime

def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


# Some error
@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")
    db, cur = get_db()

    if user_id is None:
        g.user = None
    else:
        cur.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        g.user = (
            cur.fetchone()
            #  The fetchone () and fetchall () are the methods of Python MySQL connector and they are used to display
            #   data. This connector helps in enabling the Python programs to use MySQL databases.
        )


@bp.route("/register", methods=("GET", "POST"))
def register():
    """Register a new user.

    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db, cur = get_db()
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."

        if error is None:
            try:
                # Nickname inserted the same as username
                cur.execute(
                    "INSERT INTO users (username, nickname, password) VALUES (%s, %s, %s)",
                    (username, username, generate_password_hash(password)),
                )
                db.commit()
            except Exception as e:
                # The username was already taken, which caused the
                # commit to fail. Show a validation error.
                print(e)
                error = f"Username {username} is already registered, try again!"
            else:
                # Success, go to the login page.
                flash("Thank you for registration!")
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db, cur = get_db()
        error = None
        cur.execute(
            "SELECT * FROM Users WHERE username = %s", (username,)
        )
        user = cur.fetchone()
        # print('***', user["password"], password)

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session["user_id"] = user["user_id"]
            return redirect(url_for("core.index"))

        flash(error)

    return render_template("auth/login.html")

@bp.route("/adminlogin", methods=("GET", "POST"))
def adminlogin():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db, cur = get_db()
        error = None
        cur.execute(
            """SELECT *
               FROM 
               (
               SELECT * 
               FROM Users 
               WHERE username = %s)a
               INNER JOIN admin 
               ON a.user_id=admin.user_id """, (username,)
        )
        user = cur.fetchone()
        # print('***', user["password"], password)

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session["user_id"] = user["user_id"]
            session['admin_id'] = user["admin_id"]
            return redirect(url_for("admin.index"))

        flash(error)

    return render_template("auth/adminlogin.html")


@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("core.index"))