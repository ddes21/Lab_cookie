from flask import Blueprint, current_app, request, redirect, make_response, render_template
from datetime import datetime
import base64

main_bp = Blueprint("main", __name__)

## Global last login just for the lols
LAST_LOGINS = {}

@main_bp.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        users = current_app.config["USERS"]
        if username in users and users[username] == password:

            # record login time
            LAST_LOGINS[username] = {
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "ip": request.remote_addr
            }


            encoded_user = base64.b64encode(username.encode()).decode()
            resp = make_response(redirect("/user"))
            resp.set_cookie("user", encoded_user)
            return resp

        return "Invalid credentials", 401

    return render_template("login.html")

@main_bp.route("/user")
def user_page():
    cookie = request.cookies.get("user")
    if not cookie:
        return redirect("/")

    try:
        decoded_user = base64.b64decode(cookie.encode()).decode()
    except Exception:
        return "Invalid cookie", 400
    
    info = LAST_LOGINS.get(decoded_user)

    return render_template("user.html", username=decoded_user, login_info=info)

@main_bp.route("/admin")
def admin_page():
    cookie = request.cookies.get("user")
    if not cookie:
        return redirect("/")

    try:
        decoded_user = base64.b64decode(cookie.encode()).decode()
    except Exception:
        return "Invalid cookie", 400

    # Vulnerable check: just trusts the cookie (matches original behavior)
    if decoded_user == "admin":
        return render_template("admin.html")
    else:
        return render_template("access_denied.html")

@main_bp.route("/logout")
def logout():
    resp = make_response(redirect("/"))
    resp.set_cookie("user", "", expires=0)
    return resp
