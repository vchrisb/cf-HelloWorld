"""Cloud Foundry test"""
from flask import Flask, render_template, Markup
import os
import json

app = Flask(__name__)

COLOR = "#33CC33"

# get CF environment variables
port = int(os.getenv("PORT"))

VCAP_APPLICATION = json.loads(os.environ['VCAP_APPLICATION'])
app_instance = int(VCAP_APPLICATION['instance_index'])
app_guid = VCAP_APPLICATION['application_id']
app_name = VCAP_APPLICATION['application_name']

content = '<h1>Hello World!</h1></br>I am instance <strong>#' + str(app_instance) + '</strong> serving application <strong>' + app_name + '</strong> with GUID <strong> ' + app_guid + ' !'
content = Markup(content)

@app.route('/')
def hello_world():
    return render_template("index.html",bgcolor=COLOR,content=content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
