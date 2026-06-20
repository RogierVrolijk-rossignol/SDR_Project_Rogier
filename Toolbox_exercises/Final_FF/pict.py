import sys
from pprint import pprint as ppp
 
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QDoubleValidator, QIntValidator
from PyQt6.QtWidgets import (
	QApplication,
	QMainWindow,
	QPushButton,
	QVBoxLayout,
	QHBoxLayout,
	QWidget,
	QLineEdit,
	QTableWidget, QTableWidgetItem,
)
 
import oopsql
 
# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
 
		self.setWindowTitle("All together now")
		self.setFixedWidth(500)
		self.setFixedHeight(500)
		
		mainwidget = QWidget()
		mainlayout = QVBoxLayout()
		mainlayout.setContentsMargins(10,10,10,10)
		mainlayout.setSpacing(10)
		
		self.what = QLineEdit()
		self.what.setPlaceholderText("what")
		mainlayout.addWidget(self.what)
		
		self.when = QLineEdit()
		self.when.setValidator(QIntValidator())
		self.when.setPlaceholderText("when")
		mainlayout.addWidget(self.when)
		
		button = QPushButton("Search")
		button.setStyleSheet("background-color: rgb(64, 200, 0); color: #ffffff; border-radius: 10; border: 2px solid black;")
		button.setFixedHeight(30)
		# FIXED
			# Now when "search" button is pressed it will start to run the 
			# "show_movies" function, PyQt6 will process this into the GUI.
		button.clicked.connect(self.show_movies)
		mainlayout.addWidget(button)
		
		self.table = QTableWidget()
		self.table.verticalHeader().hide()
		self.table.horizontalHeader().show()
		self.table.setAutoScroll(True)
		mainlayout.addWidget(self.table)
		
		mainlayout.addStretch()
		
		mainwidget.setLayout(mainlayout)
		self.setCentralWidget(mainwidget)
		
	def show_movies(self):
		title = f"%{self.what.text()}%"
		try:
			year = int(self.when.text())
		except:
			return
 
		sqlclass = oopsql.MySqliteClass('movies.db')
		sql = """
			SELECT * FROM movies
			WHERE title LIKE ? AND year LIKE ?
		"""
		rows = sqlclass.get_rows(sql, (title, year))
		self.table.clear()
		self.table.setRowCount(len(rows))
		# FIXED
		# Now the GUI shows two columns instead of one
		self.table.setColumnCount(2)
		# FIXED
		# Now the first column is "Year" and the second
		# contains "Title".
		self.table.setHorizontalHeaderLabels(['Year', 'Title'])
		y = 0
		for row in rows:
			# FIXED
			# Applies the years for each title that contains the query
			# content into column 0 (first column), with title "Year".
			#  String is applied for 'year' content, otherwise not shown
			# in GUI.
			self.table.setItem(y, 0, QTableWidgetItem(str(row['year'])))
			# FIXED
			# Applies the titles for each title that contains the query
			# content into column 1 (second column), with title "Title"
			self.table.setItem(y, 1, QTableWidgetItem(row['title']))
			y += 1
		
		self.table.resizeColumnToContents(0)
		self.table.resizeRowsToContents()
		self.table.horizontalHeader().setStretchLastSection(True)
			
 
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
