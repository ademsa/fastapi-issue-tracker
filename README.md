# FastAPI Issue Tracker

A very basic Issue Tracker REST API built using FastAPI


### Installation and Usage (Ubuntu OS)

`cd ~`

`mkdir fastapi-issue-tracker-files`

`cd ~/fastapi-issue-tracker-files`

`git clone git@github.com:ademsa/fastapi-issue-tracker.git`

`sudo apt-get install libpq-dev`

`virtualenv --python=python3 fastapi-issue-tracker-env`

`source ~/fastapi-issue-tracker-files/fastapi-issue-tracker-env/bin/activate`

`pip install poetry`

cd `~/fastapi-issue-tracker-files/fastapi-issue-tracker`

`poetry install`

`cp ./fastapi_issue_tracker/.env.example ./fastapi_issue_tracker/.env`

To set env variables:

`nano ./fastapi_issue_tracker/.env`

`poetry run app`

Optional for development purposes (lint):

`make lint`