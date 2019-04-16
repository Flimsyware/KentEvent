import sqlite3
from flaskr.Database.UniversityDB import UniversityDB,CreateUniversityTableText
from flaskr.Database.UserDB import UserDB,CreateUserTableText
from flaskr.Database.EventDB import EventDB,CreateEventTableText

# conn = sqlite3.connect(':memory:')





class DBHelper:
    selectAll = "*"
    DUPLICATE_EMAIL_ERROR = "Duplicate email error for registration."
    REGISTRATION_FIELDS_INCOMPLETE = "Registration fields were not complete."
    REGISTRATION_SUCCESS = "Registration was a success."
    LOGIN_SUCCESS = "Login was successful."
    LOGIN_FAILED = "Login was not successful."	
    QUERY_FAILED = "Query failed."
    def __init__(self):
        self.conn = sqlite3.connect("database.db", check_same_thread=False)
        self.c = self.conn.cursor()
        self.__CreateTablesIfNotExists__()
        self.__AddTestableInformationToDatabase__()
        self.__DatabaseTestingFunction__()

    def __CreateTablesIfNotExists__(self):
        self.c.execute(CreateUniversityTableText)
        self.c.execute(CreateUserTableText)
        self.c.execute(CreateEventTableText)
        self.conn.commit()

    def __AddTestableInformationToDatabase__(self):
        self.AddUser(UserDB("TestEmail1@kent.edu","TestPassword1",UserDB.dbRoleUser))
        self.AddUser(UserDB("TestEmail2@kent.edu","TestPassword2",UserDB.dbRoleUser))
        self.AddUser(UserDB("TestEmail3@kent.edu","TestPassword3",UserDB.dbRoleUser))
        self.AddUser(UserDB("TestEmail4@kent.edu","TestPassword4",UserDB.dbRoleHost))
        self.AddUser(UserDB("TestEmail5@kent.edu","TestPassword5",UserDB.dbRoleHost))
        self.AddUser(UserDB("TestEmail6@kent.edu","TestPassword6",UserDB.dbRoleHost))
    
    #The only parameters that should be dynamic are the whereValues. everything else should come from class variables
    def __SelectQuery__(self, selectArray, tableName, whereTypes, whereValues):
        selectText = "Select "

        #adds all the select arrays to the text
        for i,select in enumerate(selectArray,0):
            selectText = selectText + select
            if i != len(selectArray) - 1:
                selectText = selectText + ","
        
        #adds the from with the table name
        selectText = selectText + " From {} ".format(tableName)

        #checks if inserted any where types and if not, query and return the select from
        if len(whereTypes) == 0:
            #print(selectText)
            self.c.execute(selectText + ';')
            return self.c.fetchall()
        
        #if wheretypes is not 0 but they dont match in 
        if len(whereTypes) != len(whereValues):
            return self.QUERY_FAILED
        
        selectText = selectText + "where ("

        
        for i,where in enumerate(whereTypes,0):
            selectText = selectText + where
            if i != len(whereTypes) - 1:
                selectText = selectText + ","
        
        selectText = selectText + ") = (?"

        args = (whereValues[0],)
        for i in range(1,len(whereValues)):
            args = args + (whereValues[i],)
            selectText = selectText + ",?"

        selectText = selectText + ");"
        #print(selectText)
        self.c.execute(selectText,args)

        return self.c.fetchall()

    def AddUser(self,userDB):
        if userDB.email == None:
            return self.REGISTRATION_FIELDS_INCOMPLETE
        if userDB.password == None:
            return self.REGISTRATION_FIELDS_INCOMPLETE
        if userDB.role == None:
            return self.REGISTRATION_FIELDS_INCOMPLETE

        #self.c.execute("Select {} from {} where ({}) = (?);".format(UserDB.dbEmail,UserDB.tableName,UserDB.dbEmail),(userDB.email,))
        rows = self.__SelectQuery__([UserDB.dbEmail],UserDB.tableName,[UserDB.dbEmail],[userDB.email])
        #print(rows)

        if len(rows) > 0:
            return self.DUPLICATE_EMAIL_ERROR

        self.c.execute("Insert into User ({},{},{}) values (?,?,?);".format(UserDB.dbEmail,UserDB.dbPassword,UserDB.dbRoleEnumName),(userDB.email,userDB.password,userDB.role))
        self.conn.commit()
        return self.REGISTRATION_SUCCESS

    def Login(self,email,password):
        if email == None:
            return self.LOGIN_FAILED
        if password == None:
            return self.LOGIN_FAILED


        #self.c.execute("Select * from {} where ({},{}) = (?,?);".format(UserDB.tableName,UserDB.dbEmail,UserDB.dbPassword),(email,password))
        rows = self.__SelectQuery__([self.selectAll],UserDB.tableName,[UserDB.dbEmail,UserDB.dbPassword],[email,password])

        if len(rows) > 0:
            return self.LOGIN_SUCCESS
        else:
            return self.LOGIN_FAILED

    def close_db(self):
        self.conn.close()

    def __DatabaseTestingFunction__(self):
        print("Debugging and testing function goes here")


        print("Testing successful")
