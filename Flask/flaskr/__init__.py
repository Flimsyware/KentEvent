import os
from flask import Flask , render_template, request
from flask_bootstrap import Bootstrap
from flaskr.db import DBQueryHelper,DB
from flaskr.DatabaseClasses.UserDB import UserDB
from flask_sqlalchemy  import SQLAlchemy
import sshtunnel

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    ############################################
    #Creating database session
    tunnel = sshtunnel.SSHTunnelForwarder(
        ('ssh.pythonanywhere.com'), ssh_username="flimsyware",ssh_password="flimsythefish",
        remote_bind_address=('flimsyware.mysql.pythonanywhere-services.com',3306)
    )
    tunnel.start()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://flimsyware:flimsydatabase@127.0.0.1:{}/flimsyware$default'.format(tunnel.local_bind_port)
    DB = SQLAlchemy(app)
    
    DBQuery = DBQueryHelper(DB)
    ##############################################

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
            newUser = UserDB()
            newUser.email = str(request.form['email'])
            newUser.password = str(request.form['password'])
            loggedIn = DBQuery.Login(newUser)
            if loggedIn == True:
                return render_template("events.html")

        return render_template("login.html")

    #Registration page 
    @app.route('/register', methods=['GET', 'POST'])
    def Register():
        stringy = "false"
        if request.method == "POST":
            stringy = "true"
            newUser = UserDB()
            newUser.email = str(request.form['email'])
            newUser.password = str(request.form['password'])
            #newUser.role = str(request.form['role']
            result = DBQuery.AddUser(newUser)
            print(result)
            if result == DBQuery.REGISTRATION_SUCCESS:
                
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