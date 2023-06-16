import json
from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for

APP_PORT = 8989

# Env
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask('saml2-exercise')
app.debug = True
app.secret_key = "LAJSDIFLASJFILASDJFLJSFLIJSAD"

# Saml2 & Oauth0 Setup   
oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id="EUPzt5tyl4juevihjVKxTpC5vKirtWjO",
    client_secret="xHkgKDu1lt-YT00nD0hZgQ7BVIbcdmTOcfGnI5a4fPjuSIaew3hYw4YqFPr2_-2c",
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://dev-hjzmla12jg5irgjs.us.auth0.com/.well-known/openid-configuration'
)

# Login Route.
@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
)

# Logout Route.
@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + "dev-hjzmla12jg5irgjs.us.auth0.com"
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("login", _external=True),
                "client_id": "EUPzt5tyl4juevihjVKxTpC5vKirtWjO",
            },
            quote_via=quote_plus,
        )
)

# The login Callback
@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")

# Home Page Route
@app.route('/')
def default():
    if 'user' not in session:
        return redirect(url_for('login'))
    else:
        return '<h1>Hello, World!</h1>'

if __name__ == "__main__":
    app.run(host='::', port=str(APP_PORT))
