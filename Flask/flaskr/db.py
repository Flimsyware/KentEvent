import sqlite3
from flask import current_app, session
from flaskr.Database.UniversityDB import UniversityDB,CreateUniversityTableText
from flaskr.Database.UserDB import UserDB,CreateUserTableText
from flaskr.Database.EventDB import EventDB,CreateEventTableText
from flaskr.SessionGlobals import *

class _DBHelper:
    selectAll = "*"
    DUPLICATE_EMAIL_ERROR = "Duplicate email error for registration."
    INVALID_EMAIL_ERROR = "Input is not an email."
    NOT_KENT_EMAIL_FOR_CREATOR = "Email is not a kent email for a creator."
    REGISTRATION_FIELDS_INCOMPLETE = "Registration fields were not complete."
    REGISTRATION_SUCCESS = "Registration was a success."
    EVENT_CREATION_MISSING_FIELD = "Missing field from event."
    LOGIN_SUCCESS = "Login was successful."
    LOGIN_FAILED = "Login was not successful."	
    QUERY_FAILED = "Query failed."
    def __init__(self):
        self.conn = sqlite3.connect(
            current_app.config['DATABASE'], 
            check_same_thread=False
        )
        self.c = self.conn.cursor()
        self.__CreateTablesIfNotExists__()
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

        if(len(self.getAllEvent()) == 0):
            event1 = EventDB()
            event1.ID = 1
            event1.name = "event1"
            event1.creatorID = session[SessUserID]
            event1.description = "This is test event 1"
            event1.startTime = "5:00"
            event1.endTime = "10:00"
            event1.date = "4/28/19"
            event1.address = "kent state student center"
            event1.creationDate = "now"
            event1.creationTime = "now" 
            event1.roomNumber = 1
            event1.cost = "free"
            event2 = EventDB()
            event2.ID = 2
            event2.name = "event2"
            event2.description = "This is test event 2"
            event2.creatorID = session[SessUserID]
            event2.startTime = "1:00"
            event2.endTime = "3:30"
            event2.date = "4/28/19"
            event2.address = "bowman hall"
            event2.creationDate = "now"
            event2.creationTime = "now"
            event2.roomNumber = 217
            event2.cost = "$5.00"

            self.AddEvent(event1)
            self.AddEvent(event2)

        
    
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
            return [self.c.fetchall(),self.c.description]

        #if wheretypes is not 0 but they dont match in
        if len(whereTypes) != len(whereValues):
            return self.QUERY_FAILED

        selectText = selectText + "where "


        for i,where in enumerate(whereTypes,0):
            selectText = selectText + where + " = ?"
            if i != len(whereTypes) - 1:
                selectText = selectText + " AND "

        args = (whereValues[0],)
        for i in range(1,len(whereValues)):
            args = args + (whereValues[i],)

        selectText = selectText + ";"
        self.c.execute(selectText,args)

        return [self.c.fetchall(),self.c.description]

    def AddEvent(self,eventDB):
        if eventDB.name == None:
            return self.EVENT_CREATION_MISSING_FIELD
        #if eventDB.universityID == None:
            #return self.EVENT_CREATION_MISSING_FIELD
        if eventDB.creatorID == None:
            return self.EVENT_CREATION_MISSING_FIELD
        if eventDB.address == None:
            return self.EVENT_CREATION_MISSING_FIELD
        if eventDB.startTime == None:
            return self.EVENT_CREATION_MISSING_FIELD
        if eventDB.endTime == None:
            return self.EVENT_CREATION_MISSING_FIELD
        if eventDB.date == None:
            return self.EVENT_CREATION_MISSING_FIELD
        if eventDB.creationDate == None:
            return self.EVENT_CREATION_MISSING_FIELD
        if eventDB.creationTime == None:
            return self.EVENT_CREATION_MISSING_FIELD


        
        eventArgs = (
            eventDB.name, eventDB.creatorID, eventDB.address,\
            eventDB.description, eventDB.startTime, eventDB.endTime, eventDB.date, eventDB.creationDate,\
            eventDB.creationTime, eventDB.cost, eventDB.roomNumber)

        text = "Insert into {} ({},{},{},{},{},{},{},{},{},{},{}) values (?,?,?,?,?,?,?,?,?,?,?)".format(EventDB.tableName,\
            EventDB.dbName, EventDB.dbCreatorID,EventDB.dbAddress,\
            EventDB.dbDescription, EventDB.dbStartTime, EventDB.dbEndTime, EventDB.dbDate, EventDB.dbCreationDate,\
            EventDB.dbCreationTime, EventDB.dbCost, EventDB.dbRoomNumber)
        self.c.execute(text,eventArgs )
        self.conn.commit()
        

    def getAllEvent(self):
        #tableName, whereTypes, whereValues
        results = self.__SelectQuery__([self.selectAll],EventDB.tableName,[],[])
        newResult = []
        for event in results[0]:
            eventDict = {}
            for eventElement, eventElementName in zip(event,results[1]):
                eventDict[eventElementName[0]] = eventElement
            
            newResult.append(eventDict)

        return newResult

    def AddUser(self,userDB):
        if userDB.email == None:
            return self.REGISTRATION_FIELDS_INCOMPLETE
        if userDB.validEmail == False:
            return self.INVALID_EMAIL_ERROR
        if userDB.email.upper().endswith("@kent.edu".upper()) == False and userDB.role == UserDB.dbRoleHost:
            return self.NOT_KENT_EMAIL_FOR_CREATOR
        if userDB.password == None:
            return self.REGISTRATION_FIELDS_INCOMPLETE
        if userDB.role == None:
            return self.REGISTRATION_FIELDS_INCOMPLETE

        #self.c.execute("Select {} from {} where ({}) = (?);".format(UserDB.dbEmail,UserDB.tableName,UserDB.dbEmail),(userDB.email,))
        rows = self.__SelectQuery__([UserDB.dbEmail],UserDB.tableName,[UserDB.dbEmail],[userDB.email])[0]
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
        rows= self.__SelectQuery__([UserDB.dbID,UserDB.dbRoleEnumName],UserDB.tableName,[UserDB.dbEmail,UserDB.dbPassword],[email,password])[0]

        if len(rows) > 0:
            session[SessLoggedIn] = True
            session[SessUserID] = rows[0][0]
            session[SessUserType] = rows[0][1]
            return self.LOGIN_SUCCESS
        else:
            session['logged_in'] = False
            return self.LOGIN_FAILED

    def close_db(self):
        self.conn.close()

    def __DatabaseTestingFunction__(self):
        print("Debugging and testing function goes here")


        print("Testing successful")

_cachedHelper = None

def getDbHelper():
    global _cachedHelper
    if _cachedHelper == None:
        _cachedHelper = _DBHelper()
    return _cachedHelper
