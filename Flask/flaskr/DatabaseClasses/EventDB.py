class EventDB:
    #This is the actual name of the variables in the database table
    tableName = "Event"
    dbID = "ID"
    dbUniversityID = "UniversityID"
    dbCreatorID = "CreatorID"
    dbDescription = "Description"
    dbStartTime = "StartTime"
    dbEndTime = "EndTime"
    dbDate = "Date"
    dbCreationDate = "CreationDate"
    dbCreationTime = "CreationTime"
    dbCost = "Cost"
    dbRoomNumber = "RoomNumber"
    
    def __init__(self):
        self.ID = None
        self.universityID = None
        self.creatorID = None
        self.description = None
        self.startTIme = None
        self.endTime = None
        self.date = None
        self.creationDate = None
        self.creationTime = None
        self.cost = None
        self.roomNumber = None

