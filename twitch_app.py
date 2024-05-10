from flask import Flask, redirect, request, render_template, jsonify
import requests

app = Flask(__name__)
form_data = {}

client_id = "cjozi7jsygp2hy4r988bvigyt620l8"
client_secret = "tvayerthfrppebkorki2qdko4fl8by"
token_url = "https://id.twitch.tv/oauth2/token"
user_url = "https://api.twitch.tv/helix/users"

session = requests.Session()

@app.route("/form", methods=["GET"])
def form_get():
    return render_template("form.html", data=form_data)
@app.route("/form", methods=["POST"])
def form_post():
    form_data = request.form.to_dict()
    return redirect("/form")
def get_twitch_token():
    token_data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "authorization_code",
        "code": request.args.get("code"),
        "redirect_uri": "http://localhost:5000/form"
    }

    response = session.post(token_url, data=token_data)
    response.raise_for_status()
    return response.json()["access_token"]
def get_twitch_user(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Client-ID": client_id
    }

    response = session.get(user_url, headers=headers)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    app.run(debug=True)