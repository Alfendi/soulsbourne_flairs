from flask import Flask, abort, request, render_template, redirect, url_for
from praw.util.token_manager import BaseTokenManager
from uuid import uuid4
from classes import *
from config import *
import requests
import requests.auth
import urllib.parse

app = Flask(__name__, template_folder="template", static_folder='static')
app.config['SECRET_KEY'] = SECRET_KEY

login_manager = LoginManager()
refresh_token_manager = customTokenManager()

saved_state = ""
subreddit_names = ["demonssouls", "darksouls", "DarkSouls2", "bloodborne"]


def save_created_state(state):
    global saved_state
    saved_state = state


def is_valid_state(state):
    global saved_state
    if saved_state == state:
        return True
    else:
        return False


@app.route('/', methods=['GET', 'POST'])
def homepage():
    if login_manager.get_state():
        form = FlairChange(request.form)
        return redirect(url_for('change_flair'))
    return redirect(url_for('verification'))


@app.route("/verification", methods=['GET', 'POST'])
def verification():
    form = Verification(request.form)
    if form.validate_on_submit():
        passkey = request.form.get("passkey")
        if passkey == PASSKEY:
            login_manager.set_verified()
            return redirect(make_authorization_url())
    return render_template('verification.html', form=form)


@app.route("/flair", methods=['GET', 'POST'])
def change_flair():
    form = FlairChange(request.form)
    if form.validate_on_submit():
        user_to_edit = request.form.get("name")
        games = form.flairs.data
        new_flair_text = flair_text(games)
        new_flair_css_class = flair_css_class(games)
        for subreddit_name in subreddit_names:
            subreddit = r.subreddit(subreddit_name)
            subreddit.flair.set(redditor=user_to_edit, text=new_flair_text, css_class=new_flair_css_class)
        return redirect(url_for('confirmation'))
    return render_template('flair.html', form=form)


def flair_text(games):
    result_string = ''.join(games)
    print(result_string)
    return result_string


def flair_css_class(games):
    list = [item.replace(':', '') for item in games]
    modified_list = []
    exception = "Sek"
    for item in list:
        if item == exception:
            modified_list.append(item)
        else:
            modified_list.append(item.replace("S", ""))
    modified_list.append('T')
    result_string = ''.join(modified_list)
    print(result_string)
    return result_string


@app.route("/confirmation", methods=['GET', 'POST'])
def confirmation():
    return render_template('confirmation.html')


@app.route("/error", methods=['GET', 'POST'])
def error():
    return render_template('error.html')


def make_authorization_url():
    scopes = ["*"]
    state = str(uuid4())
    save_created_state(state)
    url = auth_r.auth.url(scopes, state, "permanent")
    return url


@app.route('/reddit_callback')
def reddit_callback():
    error = request.args.get('error', '')
    if error:
        return "Error: " + error
    state = request.args.get('state', '')
    if not is_valid_state(state):
        abort(403)
    code = request.args.get('code')
    refresh_token = auth_r.auth.authorize(code)
    if refresh_token == '':
        user = auth_r.user.me()
    else:
        refresh_token_manager.set_initial_token(refresh_token)
        user = r.user.me()
    return redirect(url_for('change_flair'))


if __name__ == "__main__":
    auth_r = praw.Reddit(client_id=CLIENT_ID,
                         client_secret=CLIENT_SECRET,
                         redirect_uri=REDIRECT_URI,
                         user_agent=USER_AGENT)

    r = praw.Reddit(client_id=CLIENT_ID,
                    client_secret=CLIENT_SECRET,
                    token_manager=refresh_token_manager,
                    user_agent=USER_AGENT)
    app.run(debug=True, port=8080)
