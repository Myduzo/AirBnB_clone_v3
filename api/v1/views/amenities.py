#!/usr/bin/python3
""" Creates a view for Amenity objects """

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET", "POST"],
                 strict_slashes=False)
def amenities():
    """GET and POST requests"""
    if request.method == "GET":
        all_amenities = storage.all(Amenity).values()
        my_list = []
        for value in all_amenities:
            my_list.append(value.to_dict())
        return jsonify(my_list)
    else:
        r = request.get_json()
        if r is None:
            return "Not a JSON", 400
        if "name" is None:
            return "Missing name", 400
        amenity = Amenity()
        for key, value in r.items():
            setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def amenities_id(amenity_id):
    """GET, PUT and DELETE requests"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    elif request.method == "GET":
        return jsonify(amenity.to_dict())
    elif request.method == "DELETE":
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        r = request.get_json()
        if r is None:
            return "Not a JSON", 400
        for key, value in r.items():
            if key != "id" and key != "created_at" and key != "updated_at":
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict()), 200
