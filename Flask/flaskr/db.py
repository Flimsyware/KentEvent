import sqlite3
from flaskr.Database.UniversityDB import UniversityDB,CreateUniversityTableText
from flaskr.Database.UserDB import UserDB,CreateUserTableText
from flaskr.Database.EventDB import EventDB,CreateEventTableText

# conn = sqlite3.connect(':memory:')


class DBHelper:
    def __init__(self):
        self.conn = sqlite3.connect("database.db", check_same_thread=False)
        self.c = self.conn.cursor()

    def CreateTablesIfNotExists(self):
        self.c.execute(CreateUniversityTableText)
        self.c.execute(CreateUserTableText)
        self.c.execute(CreateEventTableText)
        self.conn.commit()


    DUPLICATE_EMAIL_ERROR = "Duplicate email error for registration."
    REGISTRATION_FIELDS_INCOMPLETE = "Registration fields were not complete."
    REGISTRATION_SUCCESS = "Registration was a success."
    LOGIN_SUCCESS = "Login was successful."
    LOGIN_FAILED = "Login was not successful."	

        #TODO: This needs to be modular and not just query one thing
        #---Should have array of select, the table name, array for where and the array for values simple
        #---the arrays must be ordered.
    def Query(self):
        print("nothing")

    def AddUser(self,userDB):
        if userDB.email == None:
            return self.REGISTRATION_FIELDS_INCOMPLETE
        if userDB.password == None:
            return self.REGISTRATION_FIELDS_INCOMPLETE
        if userDB.role == None:
            return self.REGISTRATION_FIELDS_INCOMPLETE

        self.c.execute("Select {} from {} where ({}) = (?);".format(UserDB.dbEmail,UserDB.tableName,UserDB.dbEmail),(userDB.email,))
        rows = self.c.fetchall()
        print(rows)

        if len(rows) > 0:
            return self.DUPLICATE_EMAIL_ERROR

        self.c.execute("Insert into User ({},{},{}) values (?,?,?);".format(UserDB.dbEmail,UserDB.dbPassword,UserDB.dbRole),(userDB.email,userDB.password,userDB.role))
        self.conn.commit()
        return self.REGISTRATION_SUCCESS

    def Login(self,email,password):
        if email == None:
            return self.LOGIN_FAILED
        if password == None:
            return self.LOGIN_FAILED


        self.c.execute("Select * from {} where ({},{}) = (?,?);".format(UserDB.tableName,UserDB.dbEmail,UserDB.dbPassword),(email,password))
        rows = self.c.fetchall()

        if len(rows) > 0:
            return self.LOGIN_SUCCESS
        else:
            return self.LOGIN_FAILED

    def close_db(self):
        self.conn.close()