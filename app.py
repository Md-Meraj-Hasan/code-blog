from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

code_data = ""
image_path = ""

@app.route("/")
def home():
    return render_template("index.html", code=code_data, image=image_path)


@app.route("/admin", methods=["GET","POST"])
def admin():

    global code_data, image_path

    if request.method == "POST":

        code_data = request.form["code"]

        file = request.files["image"]

        if file and file.filename != "":

            filename = file.filename

            path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

            file.save(path)

            image_path = "static/uploads/" + filename

        return redirect(url_for("home"))

    return render_template("admin.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
