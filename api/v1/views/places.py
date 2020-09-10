#!/usr/bin/python3
"""
view for places objects that handles
all default RestFul API actions
"""

from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models.place import Place
from models.city import City


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def all_places(city_id):
    """Retrieves the list of all Place objects"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    list_places = []
    for item in city.places:
        list_places.append(item.to_dict())
    return jsonify(list_places)


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def places_by_id(place_id):
    """Retrieves a places object"""
    all_places = storage.all("Places").values()
    for obj in all_places:
        if obj.id == place_id:
            return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_places(place_id):
    """delete places"""
    obj = storage.get('Places', place_id)
    if obj is not None:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_places(city_id):
    """create places"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    r = request.get_json()
    if r is None:
        abort(400, 'Not a JSON')
    if "user_id" not in r:
        abort(400, 'Missing user_id')
    if 'name' not in r.keys():
        abort(400, 'Missing name')
    user = storage.get("User", r["user_id"])
    if user is None:
        abort(404)

    r["city_id"] = city_id
    place = Place(**r)
    storage.new(place)
    storage.save()


@app_views.route('/places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def update_places(places_id):
    """update place"""
    obj = storage.get('Places', place_id)
    if obj is None:
        abort(404)
    r = request.get_json()
    if r is None:
        abort(400, 'Not a JSON')
    for k, v in r.items():
        if k not in['id', 'created_at', 'updated_at']:
            setattr(obj, k, v)
    storage.save()
    return jsonify(obj.to_dict()), 200
