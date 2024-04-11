import os
import redis
import time
import sentry_sdk
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

# Sentry initialization


sentry_sdk.init(
    dsn="https://a151e83cec6feb34f0b36bf6d14d0244@o4504045228720128.ingest.us.sentry.io/4507068209102848",
    enable_tracing=True,
    traces_sample_rate=1,     
    profiles_sample_rate=0.2,
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
    if session.get("user") is not None:
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
def terms_of_service():
    return render_template("public/terms-of-service.html")


@app.route("/privacy-policy")
def privacy_policy():
    return render_template("public/privacy-policy.html")


@app.route("/cancellation")
def cancelation_policy():
    return render_template("public/cancellation-policy.html")


# Auth routes


@app.route("/authentication/register")
def auth_register():
    return render_template("auth/authentication.html")


@app.route("/authentication/sign-out")
def auth_sign_out():
    session.pop("user", None)
    return redirect(url_for("index"))


# Event routes

@app.route("/events/battle-blitz")
def event_battle_blitz():
    return render_template("events/battle-blitz.html")

@app.route("/events/treasure-quest")
def event_treasure_quest():
    return render_template("events/treasure-quest.html")

@app.route("/events/code-clash")
def event_code_clash():
    return render_template("events/code-clash.html")

@app.route("/events/web-dash")
def event_web_dash():
    return render_template("events/web-dash.html")

@app.route("/events/reel-craft")
def event_reel_craft():
    return render_template("events/reel-craft.html")


# Error handlers


@app.errorhandler(404)
def page_not_found(error):
    return (
        render_template(
            "public/error.html",
            error_code=404,
            error_message="The requested page was not found.",
            error_description="The page you are looking for might have been removed, had its name changed, or is temporarily unavailable.",
        ),
        404,
    )


if __name__ == "__main__":
    app.run(debug=True)
