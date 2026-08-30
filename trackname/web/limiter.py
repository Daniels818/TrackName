"""Shared Flask-Limiter instance.

Created without an app so it can be imported by both app.py (which calls
init_app) and routes.py (which applies per-route @limiter.limit(...)
decorators) without a circular import.
"""
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
)
