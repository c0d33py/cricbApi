# Cricket API

This is a simple API for cricket scores. It uses the [Cricinfo API](http://www.espncricinfo.com/ci/content/site/cricket_api.html) to get the scores.

## Usage

### Install the package using pip

Activate your virtualenv and then run:

```sh
source bin/activate
```

Install the requirements:

```sh
pip install -r requirements.txt
```

Run the server:

```sh
gunicorn main:app --bind 0.0.0.0:8000 --workers 4
```
