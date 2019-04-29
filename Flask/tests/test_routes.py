from flask_testing import TestCase
from flask import session

from tests.conftest import getApp, getClient, RouteActions

from flaskr.Database.UserDB import UserDB
from flaskr.db import getDbHelper
from flaskr.SessionGlobals import SessLoggedIn, SessUserType, SessUserID

class TestRoutes(TestCase):
    def setUp(self):
        self.dbHelper = getDbHelper()
        self.routeActions = RouteActions()

    def create_app(self):
        return getApp()

    def test_login_should_redirect_on_successful_login(self):
        email = 'demoEmail@example.com'
        password = 'test password'
        role = 'All-powerful test user'
        self.dbHelper.AddUser(UserDB(email,password,role))
        
        result = self.routeActions.loginAction(email, password)
        
        self.assert_redirects(result, '/events')

    def test_login_should_set_session_variables_on_successful_login(self):
        # arrange
        email = 'demoEmail@example.com'
        password = 'test password'
        role = 'All-powerful test user'
        self.dbHelper.AddUser(UserDB(email,password,role))
        
        with getClient() as c:
            session[SessLoggedIn] = False
            session[SessUserID] = None
            session[SessUserType] = None

            #act
            self.routeActions.loginAction(email, password)

            assert session[SessLoggedIn] is True
            assert session[SessUserID] is not None
            assert session[SessUserType] == role

    def test_login_should_display_error_message_if_user_does_not_exist(self):
        email = 'nonexistentUser@example.com'
        password = 'not-a-real-password'
        
        self.routeActions.loginAction(email, password)
        
        self.assert_template_used("login.html")
        self.assert_context("loginCheck", self.dbHelper.LOGIN_FAILED)
    
    def test_login_should_not_set_session_variables_on_unsuccessful_login(self):
        # arrange
        email = 'demoEmail@example.com'
        password = 'test password'
        
        with getClient() as c:
            session[SessLoggedIn] = False
            session[SessUserID] = None
            session[SessUserType] = None

            #act
            self.routeActions.loginAction(email, password)

            assert SessLoggedIn not in session
            assert SessUserID not in session
            assert SessUserType not in session

    # registration should save new user credentials if they do not exist
    def test_registration(self):
        email = 'testing123@gmail.com'
        password = 'password'
        role = 'All-powerful test user'

        result = self.routeActions.registerAction(email, password, role)

        self.assert_template_used("register.html")
        self.assert_context("registrationCheck", self.dbHelper.REGISTRATION_SUCCESS)