#https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient
#pip install mysqlclient-1.4.2-cp37-cp37m-win32.whl

#https://kite.com/python/docs/sqlalchemy.engine.result.ResultProxy
from flask_sqlalchemy  import SQLAlchemy
DB = SQLAlchemy()

class DBQueryHelper:
	def __init__(self, db):
		self.DB=db

	#TODO: This needs to be modular and not just query one thing
	#---Should have array of select, the table name, array for where and the array for values simple
	#---the arrays must be ordered.
	def Query(self):
		return self.DB.engine.execute("SELECT * FROM University WHERE Name = \"Akron\";")

	def AddUser(self,userDB):
		if issubclass(type(userDB.email), str) == False:
			print("email not type of str.")
			return None
			
		if issubclass(type(userDB.password), str) == False:
			print("password not type of str.")
			return None

		if issubclass(type(userDB.role), str) == False:
			print("Role not type of str.")
			return None

		queryText = "INSERT INTO User (Email,Password,Role) "\
			"values (\"" + userDB.email + "\",\"" + userDB.password + "\",\"" + userDB.role + "\");"
		result = self.DB.engine.execute(queryText)

	def Login(self, userDB):
		if issubclass(type(userDB.email), str) == False:
			print("email not type of str.")
			return False
		
		if issubclass(type(userDB.password), str) == False:
			print("password not type of str.")
			return False

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


		
