"""Cloud Foundry test"""
import json
import os
import time
from datetime import datetime, timedelta

from flask import Flask, render_template
from flask_caching import Cache
from flask_healthz import HealthError, healthz
from markupsafe import Markup

app = Flask(__name__)
app.register_blueprint(healthz, url_prefix="/healthz")

GREEN = "#33CC33"
ORANGE = "#FFA500"
RED = "#FF0000"

config = {
    "DEBUG": os.getenv("DEBUG", default="False")
    == "True",  # some Flask specific configs
    "CACHE_TYPE": "FileSystemCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300,
    "CACHE_DIR": "cache",
    "HEALTHZ": {
        "live": "hello.liveness",
        "ready": "hello.readiness",
    },
}

app.config.from_mapping(config)
cache = Cache(app)

# get CF environment variables
port = int(os.getenv("PORT", default=8080))

default_vcap_application = '{"instance_index": 0, "application_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "application_name": "helloworld-local"}'
VCAP_APPLICATION = json.loads(
    os.getenv("VCAP_APPLICATION", default=default_vcap_application)
)

app_instance = int(VCAP_APPLICATION["instance_index"])
app_guid = VCAP_APPLICATION["application_id"]
app_name = VCAP_APPLICATION["application_name"]


@app.route("/")
def hello_world():
    fail_ready = cache.get("fail_ready")
    fail_live = cache.get("fail_live")
    content = Markup(
        "<h1>Hello World!</h1></br>I am instance <strong>#"
        + str(app_instance)
        + "</strong> serving application <strong>"
        + app_name
        + "</strong> with GUID <strong> "
        + app_guid
        + "</strong>!"
    )

    if isinstance(fail_live, bool) and fail_live:
        time.sleep(5)
        COLOR = RED
    elif isinstance(fail_ready, datetime) and fail_ready > datetime.now():
        time.sleep(1)
        COLOR = ORANGE
    else:
        COLOR = GREEN
    return render_template("index.html", bgcolor=COLOR, content=content)


@app.route("/fail/ready")
def fail_ready():
    cache.set("fail_ready", datetime.now() + timedelta(minutes=1))
    content = Markup(
        "<h1>Fail Readiness</h1></br>Readiness for instance <strong>#"
        + str(app_instance)
        + "</strong> with GUID <strong> "
        + app_guid
        + "</strong> fails until <strong>"
        + str(cache.get("fail_ready"))
        + "</strong>!"
    )

    return render_template("index.html", bgcolor=ORANGE, content=content)


@app.route("/fail/live")
def fail_live():
    cache.set("fail_live", True)
    content = Markup(
        "<h1>Fail Liveness</h1></br>Liveness for instance <strong>#"
        + str(app_instance)
        + "</strong> with GUID <strong> "
        + app_guid
        + "</strong> will fail"
        + "</strong>!"
    )

    return render_template("index.html", bgcolor=RED, content=content)


def liveness():
    with app.app_context():
        fail_live = cache.get("fail_live")
        if isinstance(fail_live, bool) and fail_live:
            raise HealthError("App ist failing")
        else:
            pass


def readiness():
    with app.app_context():
        fail_ready = cache.get("fail_ready")
        if isinstance(fail_ready, datetime) and fail_ready > datetime.now():
            raise HealthError("App ist not ready")
        else:
            pass


if __name__ == "__main__":
    with app.app_context():
        cache.clear()
    app.run(host="0.0.0.0", port=port)
