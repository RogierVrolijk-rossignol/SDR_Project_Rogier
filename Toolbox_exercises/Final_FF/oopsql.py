import sqlite3
import sys
import os
from pprint import pprint as ppp
 
class MySqliteClass:
	_path = ""
	_conn = None
	_cursor = None
	
	def __init__(self, db_path: str):
		self._path = db_path
		# connect to database at location db_path
		self.connect()
		
	def __del__(self):
		try:
			self._conn.close()
		except:
			pass
	
	def row_factory(self, cursor, row):
		# put the row factory here and make sure it works	
		d = dict()
		for idx, value in enumerate(row):
			d[cursor.description[idx][0]] = value
		return d
 
	def connect(self):
		# connects to the database and stores connection and cursor in
		# self._conn and self._cur
		if not os.path.isfile(self._path):
			sys.exit(f"No such file {self._path}")
		self._conn = sqlite3.connect(self._path)
		self._conn.row_factory = self.row_factory
		self._cursor = self._conn.cursor()
 
	def is_valid(self) -> bool:
		# test if there is a working db connection
		# always returns a boolean
		return not self._conn is None and not self._cursor is None
	
	def get_rows(self, sql: str, placeholders: tuple=()) -> list:
		# given the sql statement
		# returns a list of rows from the database
		rows = list(self._cursor.execute(sql, placeholders))
		return rows
 
class MoviesDb(MySqliteClass):
	def what_when(self, what: str, year: int) -> list:
		sql = """
			SELECT * FROM movies
			WHERE title LIKE ? AND year LIKE ?
		"""
		# FIXED
			# Now it searches for titles containing string from "what" given by the user,
			# instead of searching for the exact title given in "what".
		rows = self.get_rows(sql, (f"%{what}%", year))
		return rows


# FIXED
	# When "oopsql.py" is imported into any file (this case "pict.py"), it won't start 
	# asking the questions below since its bonded when only "oopsql.py" is running.
if __name__ == "__main__":
	mdb = MoviesDb("movies.db")
	what = input("What title? ")
	when = int(input("Year? "))
	result = mdb.what_when(what, when)
	ppp(result)
