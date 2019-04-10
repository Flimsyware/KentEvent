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
        self.email = None
        self.password = None
        self.role = "User"

    def SetEmail(inEmail):
        #Check if it is string and formatted to be an email
        #from deloziers example of formatting or something
        self.email = inEmail