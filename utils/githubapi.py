import os
import requests
from time import time, sleep

HEADERS = {
    'Accept': 'application/vnd.github+json',
    'Authorization': 'Bearer ' + os.getenv("MORCORE"),
}


def get_REPO_USER_from_github_url(url:str):
    return url.split("https://github.com/")[1]

def api_request(request_str: str) -> requests.Response:
    response = requests.get(request_str, headers=HEADERS)
    wait_api_rate_limit(response)
    return response


def wait_api_rate_limit(response: requests.Response):
    if int(response.headers["X-RateLimit-Remaining"]) <= 1:
        print(f"exceed api rate limit, waiting")
        while int(time()) <= int(response.headers["X-RateLimit-Reset"]) + 1:
            sleep(1)
        print(f"api rate limit reset")