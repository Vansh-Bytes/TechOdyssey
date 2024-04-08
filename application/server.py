import os
import redis
import time
from functools import wraps
from dotenv import load_dotenv
from pymongo import MongoClient
from flask_session import Session
from flask_social_oauth import Config, initialize_social_login
from flask import Flask, render_template, redirect, url_for, session, jsonify

# Helper functions


def is_user_authenticated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user" in session:
            return redirect(url_for("index"))
        else:
            return func(*args, **kwargs)

    return wrapper


def generate_user_session(user, provider):
    if provider == "google":
        mongodb_cursor["users"].find_one_and_update(
            {"user_email": user["email"].lower()},
            {
                "$set": {
                    "user_info": {
                        "user_name": user["name"],
                        "user_avatar_url": user["picture"],
                        "user_provider": provider,
                    },
                    "account_info": {
                        "last_login": time.time(),
                    },
                }
            },
            upsert=True,
        )
    elif provider == "github":
        mongodb_cursor["users"].find_one_and_update(
            {"user_email": user["email"].lower()},
            {
                "$set": {
                    "user_info": {
                        "user_name": user["name"],
                        "user_avatar_url": user["avatar_url"],
                        "user_provider": provider,
                    },
                    "account_info": {
                        "last_login": time.time(),
                    },
                }
            },
            upsert=True,
        )

    user_info = mongodb_cursor["users"].find_one({"user_email": user["email"].lower()})

    return {
        "id": str(user_info["_id"]),
        "email": user_info["user_email"],
        "name": user_info["user_info"]["user_name"],
        "user_avatar_url": user_info["user_info"]["user_avatar_url"],
        "provider": user_info["user_info"]["user_provider"],
    }


# Load environment variables
load_dotenv()

# Initialize MongoDB client

mongdb_connection = MongoClient(
    os.getenv("MONGODB_URI"),
)
mongodb_cursor = mongdb_connection["prod"]

# Initialize Social OAuth configuration
config = Config(
    social_auth_providers=["google", "github"],
    application_root_url="https://techodyssey.dev",
)

config.google_auth(
    google_auth_client_id=os.getenv("GOOGLE_CLIENT_ID"),
    google_auth_client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    google_auth_scope="email profile",
    google_auth_initialization_handler_uri="/authentication/initialize/google",
    google_auth_callback_handler_uri="/api/v1/authentication/handler/google",
    google_auth_initialization_handler_wrapper=is_user_authenticated,
)

config.github_auth(
    github_auth_client_id=os.getenv("GITHUB_CLIENT_ID"),
    github_auth_client_secret=os.getenv("GITHUB_CLIENT_SECRET"),
    github_auth_scope="user",
    github_auth_initialization_handler_uri="/authentication/initialize/github",
    github_auth_callback_handler_uri="/api/v1/authentication/handler/github",
    github_auth_initialization_handler_wrapper=is_user_authenticated,
)

# Initialize Flask app

app = Flask(__name__)

# Flask configuration

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# Session configuration

app.config["SESSION_TYPE"] = "redis"
app.config["SESSION_REDIS"] = redis.from_url(
    os.getenv("REDIS_URI"),
)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True
app.config["SESSION_KEY_PREFIX"] = "techodyssey-"
app.config["SESSION_COOKIE_NAME"] = "techodyssey-session"
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

# Flask OAuth initialization

initialize_social_login(session, app, config)


# Request Preprocessor


@app.before_request
def before_request():
    if "user" in session:
        if session["user"].get("provider") is None:
            if session["user"].get("verified_email") is not None:
                session["user"] = generate_user_session(session["user"], "google")
            else:
                session["user"] = generate_user_session(session["user"], "github")


# Basic routes


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


# Auth routes


@app.route("/authentication/register")
def auth_register():
    return render_template("auth/authentication.html")


@app.route("/authentication/user")
def auth_user():
    if "user" in session:
        return jsonify({"user": session["user"]})
    else:
        return redirect(url_for("auth_register"))


# Sponsors routes


@app.route("/sponsors/enquiry")
def sponsors_enquiry():
    return render_template("sponsors/enquiry.html")


if __name__ == "__main__":
    app.run(debug=True)
