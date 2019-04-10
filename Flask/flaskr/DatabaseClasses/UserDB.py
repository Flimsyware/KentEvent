
class UserDB:
    #This is the actual name of the variables in the database table
    tableName = "User"
    dbID = "ID"
    dbEmail = "Email"
    dbPassword = "Password"
    dbRole = "Role"

    def __init__(self):
        self.email = None
        self.password = None
        self.role = "User"

    def SetEmail(inEmail):
        #Check if it is string and formatted to be an email
        #from deloziers example of formatting or something
        self.email = inEmail
    
    
    