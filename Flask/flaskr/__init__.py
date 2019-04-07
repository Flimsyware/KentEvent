import os

from flask import Flask , render_template, request
from flask_bootstrap import Bootstrap
from flaskr import db

database = None
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    #Create database 
    database = db.database(app)
    #for i in database.Query():
        #print(i['Name'])


    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

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

    #Login page 
    @app.route('/login', methods=['GET', 'POST'])
    def Login():
        if request.method == "POST":
            print("Post Login")
            loggedIn = database.CheckIfUserInDB(str(request.form['username']),str(request.form['password']))
            if loggedIn == True:
                return render_template("events.html")

        return render_template("login.html")

    #Registration page 
    @app.route('/register', methods=['GET', 'POST'])
    def Register():
        stringy = "false"
        if request.method == "POST":
            stringy = "true"
            result = database.AddUser(str(request.form['username']),str(request.form['password']))
            if result != None:
                for i in result:
                    for j in i:
                        print(j)

            print("POST REGISTER")
            return render_template("register.html",stringy = stringy)
        return render_template("register.html",stringy = stringy)

    #Profile for creator 
    @app.route('/creator')
    def Creator():
        return render_template("auth/creator.html")

    #Profile for user
    @app.route('/user')
    def User():
        return render_template("user/user.html")

    #Events page
    @app.route('/events')
    def Events():
        return render_template("events.html")

    return app