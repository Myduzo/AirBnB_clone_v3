#!/usr/bin/python3
"""
index file
"""

from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage


@app_views.route("/status")
def status():
	"""returns a JSON status"""
	return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
	"""retrieves the number of each objects by type"""
	stats = {}
	stats["amenities"] = storage.count("Amenity")
	stats["cities"] = storage.count("city")
	stats["places"] = storage.count("place")
	stats["reviews"] = storage.count("review")
	stats["states"] = storage.count("state")
	stats["users"] = storage.count("user")
	return jsonify(stats)
