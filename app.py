from flask import Flask, request, redirect, make_response, render_template_string
import base64

app = Flask(__name__)

# Hardcoded credentials
USERS = {
    "user": "password123",
    "admin": "supersecret123456"
}

# Templates
LOGIN_PAGE = """
<h2>Login</h2>
<form method="POST">
  Username: <input type="text" name="username"><br>
  Password: <input type="password" name="password"><br>
  <input type="submit" value="Login">
</form>
"""

USER_PAGE = """
<h2>Welcome, {{username}}!</h2>
<p>This is the user page.</p>
<a href="/admin">Go to admin page</a><br>
<a href="/logout">Logout</a>
"""

ADMIN_PAGE = """
<h2>Admin Dashboard</h2>
<p>Welcome, Admin!</p>
<a href="/logout">Logout</a>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in USERS and USERS[username] == password:
            # Encode username in Base64 and set as cookie
            encoded_user = base64.b64encode(username.encode()).decode()
            resp = make_response(redirect("/user"))
            resp.set_cookie("user", encoded_user)
            return resp

        return "Invalid credentials", 401

    return LOGIN_PAGE

@app.route("/user")
def user_page():
    cookie = request.cookies.get("user")
    if not cookie:
        return redirect("/")
    
    try:
        decoded_user = base64.b64decode(cookie.encode()).decode()
    except Exception:
        return "Invalid cookie", 400

    return render_template_string(USER_PAGE, username=decoded_user)

@app.route("/admin")
def admin_page():
    cookie = request.cookies.get("user")
    if not cookie:
        return redirect("/")
    
    try:
        decoded_user = base64.b64decode(cookie.encode()).decode()
    except Exception:
        return "Invalid cookie", 400

    # Vulnerable check: just trusts the cookie
    if decoded_user == "admin":
        return ADMIN_PAGE
    else:
        return "Access denied", 403

@app.route("/logout")
def logout():
    resp = make_response(redirect("/"))
    resp.set_cookie("user", "", expires=0)
    return resp

if __name__ == "__main__":
    app.run(debug=True)
