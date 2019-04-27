import os
from flask import Flask , render_template, request,session,redirect
from flask_bootstrap import Bootstrap
from flaskr.db import DBHelper
from flaskr.Database.UserDB import UserDB
from flaskr.Database.EventDB import EventDB
from flaskr.SessionGlobals import *

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'database.db'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    #Database
    with app.app_context():
        dbHelper = DBHelper()

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    Bootstrap(app)

    # Landing page
    @app.route('/')
    def Landing():
        return render_template("landing.html")

   # Game page
    @app.route('/flynn')
    def Fish():
        return render_template("flynn.html")

    #Login page =============
    @app.route('/login',methods=['GET'])
    def LoginGet():
        print("Get Login")
        return render_template("login.html")

    @app.route('/login', methods=['POST'])
    def Login():
        print("Post Login")
        result = dbHelper.Login(str(request.form['email']),str(request.form['password']))
        print(session[SessLoggedIn])

        if result == DBHelper.LOGIN_SUCCESS:
            return redirect("/events")
        else:
            return render_template("login.html",loginCheck =result)

    #Registration page 
    @app.route('/register', methods=['GET', 'POST'])
    def Register():
        if request.method == "POST":
            newUser = UserDB(str(request.form['email']),str(request.form['password']),str(request.form['userType']))
            result = dbHelper.AddUser(newUser)
            print(result)
            if result == dbHelper.REGISTRATION_SUCCESS:
                #called when registration is a success.
                return render_template("register.html",registrationCheck = result)
            else:
                #called when registration was a failure.
                return render_template("register.html",registrationCheck = result)

        #called when first get on the page
        return render_template("register.html")

    #Profile for creator 
    @app.route('/creator')
    def Creator():
        listOfEvents = [eventDic1,eventDic2]
        return render_template("auth/creator.html", listOfEvents = listOfEvents)

    #Profile for user
    @app.route('/user')
    def User():
        event1 = EventDB()
        event1.ID = 1
        event1.Name = "event1"
        event1.description = "This is test event 1"
        event1.startTime = "5:00"
        event1.endTime = "10:00"
        event1.date = "4/28/19"
        event1.address = "kent state student center"
        event1.roomNumber = 1
        event1.cost = "free"
        event2 = EventDB()
        event2.ID = 2
        event2.Name = "event2"
        event2.description = "This is test event 2"
        event2.startTime = "1:00"
        event2.endTime = "3:30"
        event2.date = "4/28/19"
        event2.address = "bowman hall"
        event2.roomNumber = 217
        event2.cost = "$5.00"
        

        eventDic1 = {
			"ID" : event1.ID,
            "Name" : event1.Name,
			"Description" : event1.description,
			"StartTime" : event1.startTime,
			"EndTime" : event1.endTime,
			"Date" : event1.date,
			"Address" : event1.address,
            "RoomNumber" : event1.roomNumber,
			"Cost" : event1.cost
        }
        eventDic2 = {
            "ID" : event2.ID,
            "Name" : event2.Name,
			"Description" : event2.description,
			"StartTime" : event2.startTime,
			"EndTime" : event2.endTime,
			"Date" : event2.date,
			"Address" : event2.address,
            "RoomNumber" : event2.roomNumber,
			"Cost" : event2.cost
        }

        listOfEvents = [eventDic1,eventDic2]
        return render_template("user/user.html", listOfEvents = listOfEvents)

    #Events page
    @app.route('/events')
    def Events():
        if session.get(SessLoggedIn):
            if session[SessUserType] == UserDB.dbRoleUser:
                print("User")
                return redirect("/user")
            elif session[SessUserType] == UserDB.dbRoleHost:
                print("Host")
                return redirect("/creator")
            elif session[SessUserType] == UserDB.dbRoleAdmin:
                print("Admin")
                return redirect("/events")

        listOfEvents = [eventDic1,eventDic2]
        return render_template("events.html", listOfEvents = listOfEvents)


    @app.route('/logout')
    def Logout():
        session.clear()
        return Landing()

    

    return app

