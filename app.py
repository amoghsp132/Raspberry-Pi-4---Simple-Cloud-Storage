from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import os

app = Flask(__name__)
app.secret_key = "raspberry-secret-key"

UPLOAD_FOLDER = "storage"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

USERNAME = "admin"
PASSWORD = "raspberry"


@app.route("/", methods=["GET", "POST"])
def index():
    error = None

    # Handle login
    if request.method == "POST" and "username" in request.form:
        if request.form["username"] == USERNAME and request.form["password"] == PASSWORD:
            session["user"] = USERNAME
        else:
            error = "Invalid credentials"

    logged_in = "user" in session

    files = os.listdir(UPLOAD_FOLDER) if logged_in else []

    return render_template(
        "index.html",
        logged_in=logged_in,
        files=files,
        error=error
    )


@app.route("/upload", methods=["POST"])
def upload():
    if "user" not in session:
        return redirect(url_for("index"))

    file = request.files["file"]
    if file.filename != "":
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return redirect(url_for("index"))


@app.route("/download/<filename>")
def download(filename):
    if "user" not in session:
        return redirect(url_for("index"))

    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)


@app.route("/delete/<filename>")
def delete(filename):
    if "user" not in session:
        return redirect(url_for("index"))

    os.remove(os.path.join(UPLOAD_FOLDER, filename))
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
