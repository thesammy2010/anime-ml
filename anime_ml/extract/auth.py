# https://gitlab.com/-/snippets/2039434
import datetime
import json
import logging
import os
import secrets
from typing import Any, Dict

import requests

from anime_ml.settings import CLIENT_ID, CLIENT_SECRET


# 1. Generate a new Code Verifier / Code Challenge.
def get_new_code_verifier() -> str:
    token = secrets.token_urlsafe(100)
    return token[:128]


# 2. Print the URL needed to authorise your application.
def print_new_authorisation_url(code_challenge: str):

    url = (
        f"https://myanimelist.net/v1/oauth2/authorize?response_type=code&client_id="
        f"{CLIENT_ID}&code_challenge={code_challenge}"
    )
    logging.info(f"Authorise your application by clicking here: {url}\n")


# 3. Once you've authorised your application, you will be redirected to the webpage you've
#    specified in the API panel. The URL will contain a parameter named "code" (the Authorisation
#    Code). You need to feed that code to the application.
def generate_new_token(auth_code: str, verif_code: str) -> dict:
    # global CLIENT_ID, CLIENT_SECRET

    url = "https://myanimelist.net/v1/oauth2/token"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": auth_code,
        "code_verifier": verif_code,
        "grant_type": "authorization_code",
    }

    response = requests.post(url, data)
    response.raise_for_status()  # Check whether the requests contains errors

    token = response.json()
    response.close()
    print("Token generated successfully!")

    with open(file="token.json", mode="w") as file:
        json.dump(token, file, indent=4)
        print('Token saved in "token.json"')

    return token


# 4. Test the API by requesting your profile information
def print_user_info(access_token: str):
    url = "https://api.myanimelist.net/v2/users/@me"
    response = requests.get(url, headers={"Authorization": f"Bearer {access_token}"})

    response.raise_for_status()
    user = response.json()
    response.close()

    print(f"\n>>> Greetings {user['name']}! <<<")


def check_token() -> bool:

    token_dir: str = "token.json"

    if token_dir not in os.listdir():
        logging.info("no token downloaded")
        return False

    with open(file=token_dir, mode="r") as f:
        content: Dict[Any, Any] = json.load(fp=f)
        last_modified: datetime.datetime = datetime.datetime.fromtimestamp(os.stat(token_dir).st_mtime)
        expires_in: datetime.timedelta = datetime.timedelta(seconds=content["expires_in"])

    if not content:
        logging.warning("token file has no contents")
        return False
    elif last_modified + expires_in <= datetime.datetime.now():
        logging.info("token has expired")
        return False
    else:
        logging.info(f"Token is still valid and expires at {last_modified + expires_in}")
        return True


def authenticate():
    if not check_token():
        code_verifier = code_challenge = get_new_code_verifier()
        print_new_authorisation_url(code_challenge=code_challenge)

        authorisation_code = input("Copy-paste the Authorisation Code: ").strip()
        generated_token = generate_new_token(authorisation_code, code_verifier)

        print_user_info(generated_token["access_token"])

    else:
        return


def refresh_token():
    pass


if __name__ == "__main__":

    authenticate()
