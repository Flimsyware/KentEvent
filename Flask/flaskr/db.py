from flask_sqlalchemy  import SQLAlchemy
import sshtunnel
#https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient
#pip install mysqlclient-1.4.2-cp37-cp37m-win32.whl

#https://kite.com/python/docs/sqlalchemy.engine.result.ResultProxy

class database:
	def __init__(self,app):
		self.tunnel = sshtunnel.SSHTunnelForwarder(
			('ssh.pythonanywhere.com'), ssh_username="flimsyware",ssh_password="flimsythefish",
			remote_bind_address=('flimsyware.mysql.pythonanywhere-services.com',3306)
		)
		self.tunnel.start()
		app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://flimsyware:flimsydatabase@127.0.0.1:{}/flimsyware$default'.format(self.tunnel.local_bind_port)
		self.db = SQLAlchemy(app)

	def Query(self):
		return self.db.engine.execute("SELECT * FROM University WHERE Name = \"Akron\";")

	def AddUser(self,email,password, firstName = "John", lastName = "Doe",Role = "Guest",UniversityID = 0):
		if issubclass(type(email), str) == False:
			print("email not type of str.")
			return None
			
		if issubclass(type(password), str) == False:
			print("password not type of str.")
			return None

		if issubclass(type(firstName), str) == False:
			print("firstName not type of str.")
			return None

		if issubclass(type(lastName), str) == False:
			print("lastName not type of str.")
			return None

		if issubclass(type(Role), str) == False:
			print("Role not type of str.")
			return None

		if issubclass(type(UniversityID), int) == False:
			print("UniversityID not type of str.")
			return None

		queryText = "INSERT INTO User (Email,Password,FirstName,LastName,Role,UniversityID) "\
			"values (\"" + email + "\",\"" + password + "\",\"" + firstName + "\",\"" + lastName + "\",\"" + Role + "\",\"" + str(UniversityID) +"\");"
		result = self.db.engine.execute(queryText)

	def CheckIfUserInDB(self, email, password):
		if issubclass(type(email), str) == False:
			print("email not type of str.")
			return False
		
		if issubclass(type(password), str) == False:
			print("password not type of str.")
			return False

		queryText = "select * from User where (Email,Password) = (\"" + email + "\",\"" + password + "\");"
		result = self.db.engine.execute(queryText)
		rows = result.fetchall()

		for i in rows:
			print(i)

		if len(rows) > 0:
			print("YES")
			return True
		else:
			print("NO")
			return False


		
