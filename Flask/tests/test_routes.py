from flask_testing import TestCase

from tests.conftest import getApp, RouteActions

from flaskr.Database.UserDB import UserDB
from flaskr.db import getDbHelper

class TestRoutes(TestCase):
    def setUp(self):
        self.dbHelper = getDbHelper()
        self.routeActions = RouteActions()

    def create_app(self):
        return getApp()

    def test_login_should_work_if_user_exists(self):
        email = 'demoEmail@example.com'
        password = 'test password'
        role = 'All-powerful test user'
        self.dbHelper.AddUser(UserDB(email,password,role))
        
        result = self.routeActions.loginAction(email, password)
        
        self.assert_redirects(result, '/events')