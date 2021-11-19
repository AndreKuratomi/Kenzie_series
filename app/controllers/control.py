from flask import jsonify, request
from app.models.model import Series
from psycopg2.errorcodes import INVALID_TEXT_REPRESENTATION
from psycopg2 import errors
from ipdb import set_trace


def deco_create():
    data = request.json
    new_dict = Series(**data)
    ready = new_dict.create()

    return jsonify(ready), 201


def deco_series():
    show_everything = Series.series()

    if len(show_everything) > 0:
        return {"data": show_everything}, 200

    if len(show_everything) == 0:
        return {"data": []}, 200


def deco_select(id):
    try:
        show_just_one = Series.select_by_id(id)
        return jsonify(show_just_one), 200

    except TypeError:
        return {"message": "Não encontrado!"}, 404

    except errors.lookup(INVALID_TEXT_REPRESENTATION):
        return {"message": "Não autorizados caracteres não numéricos!"}, 400
