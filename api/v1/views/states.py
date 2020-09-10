#!/usr/bash/python3
"""
view for State objects that handles
all default RestFul API actions
"""
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """Retrieves the list of all State objects"""
    states = []
    states_values = storage.all("State").values()
    for obj in states_values:
        states.append(obj.to_dict())
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_by_id(state_id):
    """Retrieves a State object"""
    states_values = storage.all("State").values()
    for obj in states_values:
        if obj.id == state_id:
            return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object"""
    obj = storage.get('State', state_id)
    if obj is not None:
        storage.delete(obj)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a State"""
    r = request.get_json()
    if r is None:
        abort(400, 'Not a JSON')
    elif 'name' not in r.keys():
        abort(400, 'Missing name')
    else:
        c_state = State(**r)
        storage.new(c_state)
        storage.save()
        return jsonify(c_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a State object"""
    obj = storage.get('State', state_id)
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
