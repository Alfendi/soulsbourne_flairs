import config
from flask import Flask, abort, request, render_template, redirect, url_for
from uuid import uuid4
import requests
import requests.auth
import urllib.parse


def user_agent():
    return config.USER_AGENT


def base_headers():
    return {"User-Agent": user_agent()}


app = Flask(__name__, template_folder="template", static_folder='static')


@app.route('/')
def homepage():
    text = '<a href="%s">Authenticate with reddit</a>'
    return text % make_authorization_url()


def make_authorization_url():
    state = str(uuid4())
    save_created_state(state)
    params = {"client_id": config.CLIENT_ID,
              "response_type": "code",
              "state": state,
              "redirect_uri": config.REDIRECT_URI,
              "duration": "temporary",
              "scope": "identity"}
    url = "https://ssl.reddit.com/api/v1/authorize?" + urllib.parse.urlencode(params)
    return url


def save_created_state(state):
    pass


def is_valid_state(state):
    return True


@app.route('/reddit_callback')
def reddit_callback():
    error = request.args.get('error', '')
    if error:
        return "Error: " + error
    state = request.args.get('state', '')
    if not is_valid_state(state):
        abort(403)
    code = request.args.get('code')
    access_token = get_token(code)
    return "Your reddit username is: %s" % get_username(access_token)


def get_token(code):
    client_auth = requests.auth.HTTPBasicAuth(config.CLIENT_ID, config.CLIENT_SECRET)
    post_data = {"grant_type": "authorization_code",
                 "code": code,
                 "redirect_uri": config.REDIRECT_URI}
    headers = base_headers()
    response = requests.post("https://ssl.reddit.com/api/v1/access_token",
                             auth=client_auth,
                             headers=headers,
                             data=post_data)
    token_json = response.json()
    return token_json["access_token"]


def get_username(access_token):
    headers = base_headers()
    headers.update({"Authorization": "bearer " + access_token})
    response = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)
    me_json = response.json()
    return me_json['name']


if __name__ == "__main__":
    app.run(debug=True, port=8080)



