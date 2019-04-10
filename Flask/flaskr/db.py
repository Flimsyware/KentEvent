#https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient
#pip install mysqlclient-1.4.2-cp37-cp37m-win32.whl

#https://kite.com/python/docs/sqlalchemy.engine.result.ResultProxy
from flask_sqlalchemy  import SQLAlchemy
DB = SQLAlchemy()



class DBQueryHelper:
	DUPLICATE_EMAIL_ERROR = "Duplicate email error for registration."
	REGISTRATION_SUCCESS = "Registration was a success."
	LOGIN_SUCCESS = "Login was successful."
	LOGIN_FAILED = "Login was not successful."
	def __init__(self, db):
		self.DB=db
		

	#TODO: This needs to be modular and not just query one thing
	#---Should have array of select, the table name, array for where and the array for values simple
	#---the arrays must be ordered.
	def Query(self):
		return self.DB.engine.execute("SELECT * FROM University WHERE Name = \"Akron\";")

	def AddUser(self,userDB):
		checkIfCanRegisterQuery = "Select Email from User where Email = " + "\"" + userDB.email + "\";"
		rows = self.DB.engine.execute(checkIfCanRegisterQuery).fetchall()

		if len(rows) > 0:
			return self.DUPLICATE_EMAIL_ERROR

		queryText = "INSERT INTO User (Email,Password,Role) "\
			"values (\"" + userDB.email + "\",\"" + userDB.password + "\",\"" + userDB.role + "\");"
		self.DB.engine.execute(queryText)

		return self.REGISTRATION_SUCCESS

	def Login(self, userDB):
		
		queryText = "select * from User where (Email,Password) = (\"" + userDB.email + "\",\"" + userDB.password + "\");"
		result = self.DB.engine.execute(queryText)
		rows = result.fetchall()

		for i in rows:
			print(i)

		if len(rows) > 0:
			print("YES")
			return True
		else:
			print("NO")
			return False


		
