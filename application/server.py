import os
import uuid
import redis
import time
import requests
import sentry_sdk
from functools import wraps
from dotenv import load_dotenv
from pymongo import MongoClient
from flask_session import Session
from flask_social_oauth import Config, initialize_social_login
from flask import Flask, render_template, redirect, url_for, session, jsonify, request

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


def is_session_valid(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user" in session:
            return func(*args, **kwargs)
        else:
            session["next"] = request.url
            return redirect(url_for("auth_register"))

    return wrapper


def image_uploader(image):
    try:

        response = requests.post(
            "https://api.imgbb.com/1/upload",
            files={"image": image},
            data={
                "key": "34ac0186cc7075a3a6cf707006ecfef9",
                "name": f"{uuid.uuid4()}",
            },
            timeout=10,
        )

        if response.status_code != 200:
            return None

        return response.json()["data"]["url"]

    except TimeoutError:
        return None


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
    application_root_url="http://127.0.0.1:5000",
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


@app.after_request
def after_request(response):
    response.headers["Server"] = "TechOdyssey"
    if (
        request.path == "/api/v1/authentication/handler/google"
        or request.path == "/api/v1/authentication/handler/github"
    ):
        print("Redirecting to next page")
        if session.get("next") is not None:
            response = redirect(session["next"])
            session.pop("next", None)
    return response


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


# Registration routes


@app.route("/register")
@is_session_valid
def register():
    return render_template("public/register.html")


# Registration API routes


@app.route("/api/v1/register", methods=["POST"])
@is_session_valid
def api_register():
    event_reference = {
        "0": "Code Clash",
        "1": "Web Dash",
        "2": "Treasure Quest",
        "3": "Reel Craft",
        "4": "Battle Blitz: Valorant",
        "5": "Battle Blitz: BGMI Mobile",
        "6": "Battle Blitz: Free Fire",
    }

    form_data = request.form
    event_id = form_data.get("event")

    if event_id is None:
        return jsonify(
            {"status": "error", "message": "Please select an event to register."}
        )

    event_name = event_reference.get(event_id)

    if event_id in ["4", "5", "6"]:
        team_name = form_data.get("teamName")

        team_members = []

        for member in form_data.get("teamMembers").split(","):
            team_members.append(
                member.strip().lower().replace(" ", "").replace(",", "")
            )

        if len(team_members) == 0:
            return jsonify(
                {
                    "status": "error",
                    "message": "Please provide team members' email addresses, separated by commas.",
                }
            )

        if team_name is None:
            return jsonify(
                {"status": "error", "message": "Please provide a team name."}
            )

        for i in range(len(team_members)):
            if (
                team_members[i] == ","
                or team_members[i] == " "
                or team_members[i] == ""
            ):
                team_members = team_members[:i] + team_members[i + 1 :]

        if event_id == "4" and len(team_members) != 5:
            return jsonify(
                {
                    "status": "error",
                    "message": "To participate in Battle Blitz: Valorant, you need to have 5 members in your team.",
                }
            )

        if event_id in ["5", "6"] and len(team_members) != 4:
            return jsonify(
                {
                    "status": "error",
                    "message": "To participate in Battle Blitz: BGMI Mobile or Battle Blitz: Free Fire, you need to have 4 members in your team.",
                }
            )

        if session["user"]["email"].lower() not in team_members:
            return jsonify(
                {
                    "status": "error",
                    "message": "You need to be part of the team to register for the event. Please provide your email address in the team members list.",
                }
            )

        for member in team_members:
            if member.find("@") == -1:
                return jsonify(
                    {
                        "status": "error",
                        "message": "Please provide valid email addresses for all team members.",
                    }
                )

        if len(team_members) != len(set(team_members)):
            return jsonify(
                {
                    "status": "error",
                    "message": "Please provide unique email addresses for all team members.",
                }
            )

    if request.files.get("paymentScreenshot") is None:
        return jsonify(
            {"status": "error", "message": "Please provide the payment screenshot."}
        )

    payment_transaction_id = form_data.get("paymentTransactionId")
    if payment_transaction_id is None:
        return jsonify(
            {"status": "error", "message": "Please provide the payment transaction ID."}
        )

    payment_screenshot_url = image_uploader(request.files.get("paymentScreenshot"))
    if payment_screenshot_url is None:
        return jsonify(
            {
                "status": "error",
                "message": "An error occurred while uploading the payment screenshot. Please try again.",
            }
        )

    try:
        registrations = mongodb_cursor["registrations"]

        if event_id in ["4", "5", "6"]:
            existing_team = registrations.find_one(
                {
                    "event": event_name,
                    "teamName": form_data.get("teamName").strip().title(),
                }
            )
            if existing_team:
                return jsonify(
                    {
                        "status": "error",
                        "message": f"The team name `{form_data.get('teamName').strip().title()}` has already been registered for this event. Please provide a different team name.",
                    }
                )

            existing_member = registrations.find_one(
                {
                    "event": event_name,
                    "teamMembers": {"$in": form_data.get("teamMembers").split(",")},
                }
            )
            if existing_member:
                for member in existing_member["teamMembers"]:
                    for team_member in team_members:
                        if member == team_member:
                            return jsonify(
                                {
                                    "status": "error",
                                    "message": f"The email address `{member}` has already been registered for this event. Please provide a different email address.",
                                }
                            )

            registrations.insert_one(
                {
                    "event": event_name,
                    "name": form_data.get("name").strip().title(),
                    "email": form_data.get("email").strip().lower(),
                    "teamName": form_data.get("teamName").strip().title(),
                    "teamMembers": team_members,
                    "paymentScreenshot": payment_screenshot_url,
                    "paymentTransactionId": payment_transaction_id,
                    "status": "pending",
                }
            )

        else:
            if registrations.find_one(
                {"event": event_name, "email": form_data.get("email").strip().lower()}
            ):
                return jsonify(
                    {
                        "status": "error",
                        "message": "You have already registered for this event. You can view your registration status in the `My Events` section.",
                    }
                )

            registrations.insert_one(
                {
                    "event": event_name,
                    "name": form_data.get("name").strip().title(),
                    "email": form_data.get("email").strip().lower(),
                    "paymentScreenshot": payment_screenshot_url,
                    "paymentTransactionId": payment_transaction_id,
                    "status": "pending",
                }
            )

        return jsonify(
            {
                "status": "success",
                "message": "Registration successful. Please wait while our team verifies your payment.",
            }
        )

    except Exception as e:
        return jsonify(
            {
                "status": "error",
                "message": "An error occurred while registering. Please try again.",
            }
        )


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


@app.errorhandler(500)
def internal_server_error(error):
    return (
        render_template(
            "public/error.html",
            error_code=500,
            error_message="Something went wrong.",
            error_description="The server encountered a situation it doesn't know how to handle.",
        ),
        500,
    )


if __name__ == "__main__":
    app.run(debug=True)
