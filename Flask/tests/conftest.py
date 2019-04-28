import os
import tempfile

import pytest
from flaskr import create_app

_cachedApp = None

def getApp():
    global _cachedApp
    if _cachedApp is None:
        db_path = ':memory:'

        _cachedApp = create_app({
            'TESTING': True,
            'DATABASE': db_path,
        })

    return _cachedApp

def getClient():
    return getApp().test_client()

def getRunner():
    return getApp().test_cli_runner()

class RouteActions():
    def __init__(self):
        self._client = getClient()

    def landingPage(self):
        return self._client.get(
            '/'
        )

    def loginPage(self):
        return self._client.get(
            '/login'
        )

    def loginAction(self, email, password):
        return self._client.post(
            '/login',
            data={'email': email, 'password': password}
        )

    def registerPage(self):
        return self._client.get(
            '/register'
        )

    def registerAction(self, email, password):
        return self._client.post(
            '/register',
            data={'email': email, 'password': password}
        )

    def creator(self):
        return self._client.get('/creator')

    def user(self):
        return self._client.get('/user')

    def events(self):
        return self._client.get('/events')