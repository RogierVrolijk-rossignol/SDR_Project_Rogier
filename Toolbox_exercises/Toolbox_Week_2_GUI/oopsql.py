import sqlite3
import sys
import os
 
class OopSqlClass:
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
		self._cursor.execute(sql, placeholders)
		output = self._cursor.fetchall()
		return list(output)
	

	def get_record(self, sql: str) -> dict|None:
		try:
			return self.get_rows(sql)[0]
		except:
			return None