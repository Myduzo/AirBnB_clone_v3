#!/usr/bin/python3
"""
view for City objects that handles
all default RestFul API actions
"""
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'],
                 strict_slashes=False)
def all_citites(state_id):
    """Retrieves the list of all city objects"""
    state = storage.get("State", state_id)
    citites = []
    if state is not None:
        for city in state.cities:
            citites.append(city.to_dict())
        return jsonify(citites)
    abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city_by_id(city_id):
    """Retrieves a city object"""
    cities_values = storage.all("City").values()
    for obj in cities_values:
        if obj.id == city_id:
            return jsonify(obj.to_dict())
    abort(404)


@app_views.route('cities/<city_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a city object"""
    obj = storage.get('City', city_id)
    if obj is not None:
        storage.delete(obj)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('states/<state_id>/cities',
                 strict_slashes=False,
                 methods=['POST'])
def create_city(state_id):
    """create city"""
    state = storage.get("State", state_id)
    if state is not None:
        r = request.get_json()
        if r is None:
            abort(400, "Not a JSON")
        if 'name' not in r:
            abort(400, "Missing name")
        r['state_id'] = state.id
        city = City(**r)
        storage.new(city)
        storage.save()
        return (jsonify(city.to_dict()), 201)
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates a city object"""
    obj = storage.get('State', city_id)
    if obj is None:
        abort(400)
    r = request.get_json()
    if r is None:
        abort(400, 'Not a JSON')
    for k, v in r.items():
        if k not in['id', 'created_at', 'updated_at']:
            setattr(obj, k, v)
    storage.save()
    return jsonify(obj.to_dict())
