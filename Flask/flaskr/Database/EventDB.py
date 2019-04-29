CreateEventTableText = """
    CREATE TABLE if not exists Event(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name varchar(255) NOT NULL,
        CreatorID int NOT NULL,
        Address TEXT NOT NULL,
        Description TEXT,
        StartTime time NOT NULL,
        EndTime time NOT NULL,
        Date date NOT NULL,
        CreationDate date NOT NULL,
        CreationTime time NOT NULL,
        Cost int,
        RoomNumber int,
        PinStyle varchar(255),
        FOREIGN KEY (CreatorID) REFERENCES User(ID)
    )
"""
#UniversityID int NOT NULL,
#FOREIGN KEY (UniversityID) REFERENCES University(ID)

class EventDB:
    #This is the actual name of the variables in the database table
    tableName = "Event"
    dbID = "ID"
    dbName = "Name"
    #dbUniversityID = "UniversityID"
    dbCreatorID = "CreatorID"
    dbAddress = "Address"
    dbDescription = "Description"
    dbStartTime = "StartTime"
    dbEndTime = "EndTime"
    dbDate = "Date"
    dbCreationDate = "CreationDate"
    dbCreationTime = "CreationTime"
    dbCost = "Cost"
    dbRoomNumber = "RoomNumber"
    dbPinStyle = "PinStyle"
    
    def __init__(self):
        self.ID = None
        self.name = None
        #self.universityID = None
        self.creatorID = None
        self.address = None
        self.description = None
        self.startTime = None
        self.endTime = None
        self.date = None
        self.creationDate = None
        self.creationTime = None
        self.cost = None
        self.roomNumber = None
        self.pinStyle = None
