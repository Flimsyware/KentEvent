
CreateUniversityTableText = """
    CREATE TABLE if not exists University(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name varchar(255) NOT NULL UNIQUE,
        Address varchar(255) NOT NULL UNIQUE
    )
"""

class UniversityDB:
    tableName = "University"