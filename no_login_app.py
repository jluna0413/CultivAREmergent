from flask import Flask, render_template, redirect, url_for

app = Flask(__name__, template_folder="app/web/templates", static_folder="app/web/static")

@app.route("/")
def dashboard():
	return render_template("views/index.html", title="Dashboard", plants=[], strains=0, sensors=0, harvests=0, activities=[])

@app.route("/login")
def login():
	return redirect(url_for("dashboard"))

@app.route("/<path:path>")
def catch_all(path):
	return redirect(url_for("dashboard"))

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000, debug=True)
