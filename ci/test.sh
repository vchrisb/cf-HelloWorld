#!/bin/bash

set -e -x

cd source-code
python -m venv ./.venv
source .venv/bin/activate
pip install -r requirements.txt
pip install pytest
export PORT=8080
export VCAP_APPLICATION='{"application_name": "cf-helloworld", "instance_index": "0", "application_id": "f618b72c-f42c-4bc5-adc7-2ec0156ac944"}'
pytest