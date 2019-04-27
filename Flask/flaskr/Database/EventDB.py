CreateEventTableText = """
    CREATE TABLE if not exists Event(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name varchar(255) NOT NULL,
        UniversityID int NOT NULL,
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
        FOREIGN KEY (CreatorID) REFERENCES User(ID),
        FOREIGN KEY (UniversityID) REFERENCES University(ID)
    )
"""


class EventDB:
    #This is the actual name of the variables in the database table
    tableName = "Event"
    dbID = "ID"
    dbUniversityID = "UniversityID"
    dbCreatorID = "CreatorID"
    dbDescription = "Description"
    dbAddress = "Address"
    dbStartTime = "StartTime"
    dbEndTime = "EndTime"
    dbDate = "Date"
    dbCreationDate = "CreationDate"
    dbCreationTime = "CreationTime"
    dbCost = "Cost"
    dbRoomNumber = "RoomNumber"
    
    def __init__(self,ID,universityID,creatorID,description,address,startTime,endTime,date,creationDate,creationTime,cost,roomNumber):
        self.ID = ID
        self.universityID = universityID
        self.creatorID = creatorID
        self.description = description
        self.address = address
        self.startTIme = startTime
        self.endTime = endTime
        self.date = date
        self.creationDate = creationDate
        self.creationTime = creationTime
        self.cost = cost
        self.roomNumber = roomNumber

