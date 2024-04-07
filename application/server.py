from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("public/home.html")

@app.route("/support")
def support():
    return render_template("public/support.html")

@app.route("/terms-of-service")
def tos():
    return render_template("public/tos.html")

@app.route("/privacy-policy")
def privacy():
    return render_template("public/privacy-policy.html")

@app.route("/cancellation")
def cancellation():
    return render_template("public/cancellation.html")


if __name__ == "__main__":
    app.run(debug=True)
