#!/bin/usr/python3
"""
Web application
"""

from flask import Flask, Blueprint
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
	"""close the storage"""
	storage.close()

if __name__ == "__main__":
	app.run(host=getenv("HBNB_API_HOST"),
			port=getenv("HBNB_API_PORT"),
			threaded=True)
