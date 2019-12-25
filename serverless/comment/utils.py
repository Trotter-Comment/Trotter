import time
import random
import hashlib

from flask import (
    make_response,
    Response
)
from flask.views import MethodView

from .settings import WEBSITE
from . import app


class View(MethodView):
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']

    def dispatch_request(self, *args, **kwargs):
        resp = super().dispatch_request(*args, **kwargs)
        if not isinstance(resp, Response):
            resp = make_response(resp)

        resp.headers['Access-Control-Allow-Origin'] = ", ".join([
            WEBSITE
        ])
        resp.headers['Access-Control-Allow-Methods'] = ", ".join(self.allowed_methods())
        resp.headers["Access-Control-Allow-Credentials"] = 'true'
        resp.headers['Content-Disposition'] = 'inline'
        return resp

    def options(self):
        """Handle responding to requests for the OPTIONS HTTP verb."""
        response = make_response("", 204)
        return response

    def allowed_methods(self):
        return [m.upper() for m in self.http_method_names if hasattr(self, m)]


def route(rule, **kwargs):
    def wrapper(cls):
        app.add_url_rule(rule, view_func=cls.as_view(cls.__name__), methods=cls().allowed_methods(), **kwargs)
        return cls
    return wrapper


def ranstr() -> str:
    """random string"""
    return f'{int(time.time() * 1000)}-{random.randint(1000, 9999)}'


def get_avatar(email: str) -> str:
    md5 = hashlib.md5(email.lower().encode("utf-8")).hexdigest()
    return "https://www.gravatar.com/avatar/" + md5
