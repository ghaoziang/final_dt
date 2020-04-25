from __future__ import print_function

import requests
from flask import Flask, request, redirect
import os
from app.utils import load_config, save_config
from accesslink import AccessLink


CALLBACK_PORT = 5000
CALLBACK_ENDPOINT = "/oauth2_callback"
config_path = os.path.join(os.path.pardir, "device_config")
CONFIG_FILENAME = os.path.join(config_path, "config.yml")
REDIRECT_URL = "http://localhost:{}{}".format(CALLBACK_PORT, CALLBACK_ENDPOINT)
config = None
accesslink = None
if os.path.isfile(CONFIG_FILENAME):
    config = load_config(CONFIG_FILENAME)
    accesslink = AccessLink(client_id=config['client_id'],
                            client_secret=config['client_secret'],
                            redirect_url=REDIRECT_URL)


app = Flask(__name__)


@app.route("/")
def authorize():
    print(type(accesslink.get_authorization_url()))
    link = accesslink.get_authorization_url()
    return redirect(link)


@app.route(CALLBACK_ENDPOINT)
def callback():
    """Callback for OAuth2 authorization request
    Saves the user's id and access token to a file.
    """

    #
    # Get authorization from the callback request parameters
    #
    authorization_code = request.args.get("code")

    #
    # Get an access token for the user using the authorization code.
    #
    # The authorization code is only valid for 10 minutes, so the access token
    # should be fetched immediately after the authorization step.
    #
    token_response = accesslink.get_access_token(authorization_code)

    #
    # Save the user's id and access token to the configuration file.
    #
    config["user_id"] = token_response["x_user_id"]
    config["access_token"] = token_response["access_token"]
    save_config(config, CONFIG_FILENAME)

    #
    # Register the user as a user of the application.
    # This must be done before the user's data can be accessed through AccessLink.
    #
    try:
        accesslink.users.register(access_token=config["access_token"])
    except requests.exceptions.HTTPError as err:
        # Error 409 Conflict means that the user has already been registered for this client.
        # That error can be ignored in this example.
        if err.response.status_code != 409:
            raise err

    shutdown()
    return "Client authorized! You can now close this page."


def shutdown():
    shutdown_func = request.environ.get('werkzeug.server.shutdown')
    if shutdown_func is not None:
        shutdown_func()


def auth():
    print("Navigate to http://localhost:{port}/ for authorization.\n".format(port=CALLBACK_PORT))
    app.run(host='localhost', port=CALLBACK_PORT)
    print(CALLBACK_ENDPOINT)
