#!/usr/bin/python3
"""

"""

from api.v1.views import app_views
from flask import Flask, jsonify

@app_views.route("/status")
def status():
	"""returns a JSON status"""
	return jsonify({"status": "OK"})
