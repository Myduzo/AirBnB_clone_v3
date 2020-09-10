#!/usr/bin/python3
"""
view for Amenity objects that handles
all default RestFul API actions
"""
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    """Retrieves the list of all Amenity objects"""
    amenities = []
    amenities_values = storage.all("Amenity").values()
    for obj in amenities_values:
        amenities.append(obj.to_dict())
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def amenity_by_id(amenity_id):
    """Retrieves a Amenity object"""
    amenities_values = storage.all("Amenity").values()
    for obj in amenities_values:
        if obj.id == amenity_id:
            return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """delete amenity"""
    obj = storage.get('Amenity', amenity_id)
    if obj is not None:
        storage.delete(obj)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_Amenity():
    """create amenity"""
    r = request.get_json()
    if r is None:
        abort(400, 'Not a JSON')
    elif 'name' not in r.keys():
        abort(400, 'Missing name')
    else:
        c_Amenity = Amenity(**r)
        storage.new(c_Amenity)
        storage.save()
        return jsonify(c_Amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_Amenity(amenity_id):
    """update aminity"""
    obj = storage.get('Amenity', amenity_id)
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
