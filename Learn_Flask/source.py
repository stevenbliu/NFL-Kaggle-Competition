from flask import Flask, redirect, url_for

app = Flask(__name__)


@app.route("/")
# define the page
def home():
    return "Helllo! thisis xXCXCX <h1> the h1 tag <h!>"
    
@app.route("/page")
# define the page
def page():
    return "page! thisis xXCXCX <h1> the page tag <h!>"


#dynamic 
@app.route("/<name>")
def user(name):
    return f"Hello {name}!"

# redirect, url_for packages (redirects to a page)
@app.route("/admin")
def admin():
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run()