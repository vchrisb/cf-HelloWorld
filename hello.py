"""Cloud Foundry test"""
from flask import Flask, render_template, Markup
import os

app = Flask(__name__)

COLOR = "#33CC33"

# get CF environment variables
port = int(os.getenv("PORT"))
instance = int(os.getenv("CF_INSTANCE_INDEX"))
ip = os.getenv("CF_INSTANCE_IP")

content = '<h1>Hello World!</h1></br>I am running on instance <strong>' + str(instance) + '</strong> serving on IP <strong>' + ip + '</strong>!'
content = Markup(content)

@app.route('/')
def hello_world():
    return render_template("index.html",bgcolor=COLOR,content=content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
