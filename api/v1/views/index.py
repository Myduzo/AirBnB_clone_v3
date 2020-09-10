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
    stats["cities"] = storage.count("City")
    stats["places"] = storage.count("Place")
    stats["reviews"] = storage.count("Review")
    stats["states"] = storage.count("State")
    stats["users"] = storage.count("User")
    return jsonify(stats)
