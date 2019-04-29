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

    def test_login_should_not_work_if_user_does_not_exist(self):
        email = 'nonexistentUser@example.com'
        password = 'not-a-real-password'
        
        result = self.routeActions.loginAction(email, password)
        
        self.assert_template_used("login.html")
        self.assert_context("loginCheck", self.dbHelper.LOGIN_FAILED)

    # registration should save new user credentials if they do not exist
    def test_registration(self):
        email = 'testing123@gmail.com'
        password = 'password'
        role = 'All-powerful test user'

        result = self.routeActions.registerAction(email, password, role)

        self.assert_template_used("register.html")
        self.assert_context("registrationCheck", self.dbHelper.REGISTRATION_SUCCESS)