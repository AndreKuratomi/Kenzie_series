from flask import Flask
from app.controllers.control import deco_create, deco_series, deco_select


def init_app(app: Flask):
    app.post("/series")(deco_create)

    app.get("/series")(deco_series)

    app.get("/series/<id>")(deco_select)
