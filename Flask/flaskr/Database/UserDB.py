CreateUserTableText = """
    CREATE table if not exists User(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        GoogleToken TEXT,
        UniversityID int,
        FirstName varchar(20),
        LastName varchar(20),
        Email varchar(50) NOT NULL UNIQUE,
        Password varchar(20),
        Role varchar(10) NOT NULL,
        Bio varchar(255),
        FOREIGN KEY (UniversityID) REFERENCES University(ID)
    )
"""

class UserDB:
    #This is the actual name of the variables in the database table
    tableName = "User"
    dbID = "ID"
    dbEmail = "Email"
    dbPassword = "Password"
    dbRole = "Role"

    def __init__(self,inEmail,inPassword,inRole):
        self.SetEmail(inEmail)
        self.SetPassword(inPassword)
        self.SetRole(inRole)

    def SetEmail(self, inEmail):
        self.email = None
        #Check if it is string and formatted to be an email
        #from deloziers example of formatting or something
        if inEmail == None or inEmail == "":
            
            return False

        self.email = inEmail
        return True

    def SetPassword(self,inPassword):
        self.password = None

        #Check if password has the required characters and length
        self.password = inPassword
        return True

    def SetRole(self,inRole):
        self.role = None

        #Check if the role is the correct type
        self.role = inRole
        return True



    
    
    
    