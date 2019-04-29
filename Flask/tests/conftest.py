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
            'SECRET_KEY': 'testing',
        })

    return _cachedApp

_cachedClient = None
def getClient():
    global _cachedClient
    if _cachedClient is None:
        _cachedClient = getApp().test_client()
    return _cachedClient

_cachedRunner = None
def getRunner():
    global _cachedRunner
    if _cachedRunner is None:
        _cachedRunner = getApp().test_cli_runner()
    return _cachedRunner

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

    def registerAction(self, email, password, userType):
        return self._client.post(
            '/register',
            data={
                'email': email,
                'password': password,
                'userType': userType
            }
        )

    def creator(self):
        return self._client.get('/creator')

    def user(self):
        return self._client.get('/user')

    def events(self):
        return self._client.get('/events')