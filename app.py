from flask import Flask, render_template, redirect, session
from routes.admin_routes import admin_bp
from routes.chatbot_routes import chatbot_bp
from routes.student_routes import student_bp
from models.db import close_db

app = Flask(__name__)
app.secret_key = "secret123"


# HOME PAGE
@app.route("/")
def home():
    return render_template("choose_login.html")


# CHATBOT PAGE
@app.route("/chatbot")
def chatbot():
    return render_template("index.html")


# LOGOUT (for admin + student)
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# REGISTER ROUTES
app.register_blueprint(admin_bp)
app.register_blueprint(student_bp)
app.register_blueprint(chatbot_bp)


# CLOSE DATABASE CONNECTION
app.teardown_appcontext(close_db)


if __name__ == "__main__":
    app.run(debug=True)