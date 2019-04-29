from flask_testing import TestCase

from tests.conftest import getApp, getClient, RouteActions

from flaskr.Database.UserDB import UserDB
from flaskr.Database.EventDB import EventDB
from flaskr.db import getDbHelper
from flaskr.SessionGlobals import SessLoggedIn, SessUserType, SessUserID

class TestRoutes(TestCase):
    def setUp(self):
        self.dbHelper = getDbHelper()
        self.routeActions = RouteActions()

    def create_app(self):
        return getApp()

    def test_landing_should_return_landing_template(self):
        self.routeActions.landingPage()

        self.assert_template_used("landing.html")

    def test_flynn_should_return_flynn_template(self):
        self.routeActions.flynnPage()

        self.assert_template_used("flynn.html")

    def test_login_page_should_return_login_template(self):
        self.routeActions.loginPage()

        self.assert_template_used("login.html")

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
        
        with getClient() as client:
            with client.session_transaction() as sess:
                sess[SessLoggedIn] = False
                sess[SessUserID] = None
                sess[SessUserType] = None

            # act
            self.routeActions.loginAction(email, password)

            # assert
            with client.session_transaction() as sess:
                assert sess[SessLoggedIn] is True
                assert sess[SessUserID] is not None
                assert sess[SessUserType] == role

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
        
        with getClient() as client:
            with client.session_transaction() as sess:
                sess[SessLoggedIn] = False
                sess[SessUserID] = None
                sess[SessUserType] = None

            #act
            self.routeActions.loginAction(email, password)

            with client.session_transaction() as sess:
                assert sess[SessLoggedIn] is False
                assert sess[SessUserID] is None
                assert sess[SessUserType] is None

    def test_registration_success_on_valid_creator_email(self):
        email = 'testing123@kent.edu'
        password = 'password'
        role = 'creator'

        result = self.routeActions.registerAction(email, password, role)

        self.assert_template_used("register.html")
        self.assert_context("registrationCheck", self.dbHelper.REGISTRATION_SUCCESS)

    def test_registration_fail_on_duplicate_email(self):
        email = 'testing1234@kent.edu'
        password = 'password'
        role = 'All-powerful test user'

        self.routeActions.registerAction(email, password, role)
        self.routeActions.registerAction(email, password, role)

        self.assert_template_used("register.html")
        self.assert_context("registrationCheck", self.dbHelper.DUPLICATE_EMAIL_ERROR)

    def test_registration_fail_on_invalid_email(self):
        email = 'John Doe'
        password = 'password'
        role = 'All-powerful test user'

        result = self.routeActions.registerAction(email, password, role)

        self.assert_template_used("register.html")
        self.assert_context("registrationCheck", self.dbHelper.INVALID_EMAIL_ERROR)

    def test_registration_fail_on_email_empty(self):
        email = ''
        password = 'password'
        role = 'test user'

        result = self.routeActions.registerAction(email, password, role)

        self.assert_template_used("register.html")
        self.assert_context("registrationCheck", self.dbHelper.REGISTRATION_FIELDS_INCOMPLETE)

    def test_registration_fail_on__role_empty(self):
        email = 'testing321@example.com'
        password = 'password'
        role = ''

        result = self.routeActions.registerAction(email, password, role)

        self.assert_template_used("register.html")
        self.assert_context("registrationCheck", self.dbHelper.REGISTRATION_FIELDS_INCOMPLETE)

    def test_registration_fail_on__password_empty(self):
        email = 'testing321@example.com'
        password = ''
        role = 'user'

        result = self.routeActions.registerAction(email, password, role)

        self.assert_template_used("register.html")
        self.assert_context("registrationCheck", self.dbHelper.REGISTRATION_FIELDS_INCOMPLETE)

    def test_registration_fail_on_invalid_creator_email(self):
        email = 'test@yahoo.com'
        password = 'password'
        role = UserDB.dbRoleHost

        result = self.routeActions.registerAction(email, password, role)

        self.assert_template_used("register.html")
        self.assert_context("registrationCheck", self.dbHelper.NOT_KENT_EMAIL_FOR_CREATOR)

    def test_creator_page_should_apply_all_events_to_template(self):
        event1 = EventDB()
        event1.ID = 2424
        self.dbHelper.AddEvent(event1)
        event2 = EventDB()
        event2.ID = 1234
        self.dbHelper.AddEvent(event2)
        expectedEventList = self.dbHelper.getAllEvent()

        self.routeActions.creatorPage()

        self.assert_template_used('auth/creator.html')
        self.assert_context('listOfEvents', expectedEventList)

    def test_creator_should_add_event_to_database(self):
        event = {
            EventDB.dbName: 'name',
            EventDB.dbDescription: 'description',
            EventDB.dbAddress: 'address',
            EventDB.dbStartTime: 'start time',
            EventDB.dbEndTime: 'end time',
            EventDB.dbDate: 'date',
            EventDB.dbPinStyle: 'pin style'
        }

        with getClient() as client:
            with client.session_transaction() as sess:
                sess[SessUserID] = 'creatorID'
                sess.modified = True

            self.routeActions.creatorPost(event)

            listOfEvents = self.dbHelper.getAllEvent()
            assert len(listOfEvents) == 1
            eventAdded = listOfEvents[0]
            assert (eventAdded[EventDB.dbName] == 'name' and 
                eventAdded[EventDB.dbDescription] == 'description' and
                eventAdded[EventDB.dbAddress] == 'address' and
                eventAdded[EventDB.dbCreatorID] == 'creatorID' and
                eventAdded[EventDB.dbStartTime] == 'start time' and
                eventAdded[EventDB.dbEndTime]== 'end time' and
                eventAdded[EventDB.dbDate] == 'date' and
                eventAdded[EventDB.dbPinStyle] == 'pin style')


    def test_logout_should_clear_session_variables(self):
        with getClient() as client:
            with client.session_transaction() as sess:
                sess[SessLoggedIn] = True
                sess[SessUserID] = 1234
                sess[SessUserType] = 'user'
                sess['random variable'] = 'abc123'

            self.routeActions.logout()

            with client.session_transaction() as sess:
                assert SessLoggedIn not in sess
                assert SessUserID not in sess
                assert SessUserType not in sess
                assert 'random variable' not in sess

    def test_logout_should_redirect_to_the_root(self):
        result = self.routeActions.logout()

        self.assert_redirects(result, '/')
