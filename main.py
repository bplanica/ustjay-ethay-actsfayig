import os

import requests
from flask import Flask, send_file, Response
from bs4 import BeautifulSoup

app = Flask(__name__)


def get_fact():
    response = requests.get("http://unkno.com")
    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")

    return facts[0].get_text().strip()


@app.route('/')
def home():
    url = "https://hidden-journey-62459.herokuapp.com/piglatinize/"
    data  = {'input_text': get_fact()}

    response = requests.post(url, data=data, allow_redirects=False)
    soup = BeautifulSoup(response.content, "html.parser")
    
    headers = response.headers
    result_url = headers['Location']

    response = requests.get(result_url)
    soup = BeautifulSoup(response.content, "html.parser")

    result = soup.h2.next_sibling

    return result


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=port)