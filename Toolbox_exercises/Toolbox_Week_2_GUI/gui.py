import sys

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem
)

from oopsql import OopSqlClass


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Movie database")
        self.resize(800, 500)

        self.db = OopSqlClass("movies.db")

        main_widget = QWidget()
        main_layout = QVBoxLayout()

        input_layout = QHBoxLayout()

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Amount of movies")
        self.amount_input.setText("10")

        self.from_year_input = QLineEdit()
        self.from_year_input.setPlaceholderText("From year")
        self.from_year_input.setText("1990")

        self.to_year_input = QLineEdit()
        self.to_year_input.setPlaceholderText("To year")
        self.to_year_input.setText("1999")

        self.birth_input = QLineEdit()
        self.birth_input.setPlaceholderText("Actor born after")
        self.birth_input.setText("1970")

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_movies)

        input_layout.addWidget(QLabel("Amount:"))
        input_layout.addWidget(self.amount_input)

        input_layout.addWidget(QLabel("From:"))
        input_layout.addWidget(self.from_year_input)

        input_layout.addWidget(QLabel("To:"))
        input_layout.addWidget(self.to_year_input)

        input_layout.addWidget(QLabel("Actor born after:"))
        input_layout.addWidget(self.birth_input)

        input_layout.addWidget(self.search_button)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Title", "Year", "Rating", "Actor"])

        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.table)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def search_movies(self):
        amount = int(self.amount_input.text())
        from_year = int(self.from_year_input.text())
        to_year = int(self.to_year_input.text())
        birth_year = int(self.birth_input.text())

        query = """
        SELECT DISTINCT 
            movies.title,
            movies.year,
            ratings.rating,
            people.name
        FROM movies
        JOIN ratings ON movies.id = ratings.movie_id
        JOIN stars ON movies.id = stars.movie_id
        JOIN people ON stars.person_id = people.id
        WHERE movies.year >= ?
        AND movies.year <= ?
        AND people.birth >= ?
        ORDER BY ratings.rating DESC
        LIMIT ?
        """

        rows = self.db.get_rows(
            query,
            placeholders=(from_year, to_year, birth_year, amount)
        )

        self.table.setRowCount(0)

        for row_number, row_data in enumerate(rows):
            self.table.insertRow(row_number)

            title = str(row_data["title"])
            year = str(row_data["year"])
            rating = str(row_data["rating"])
            actor = str(row_data["name"])

            self.table.setItem(row_number, 0, QTableWidgetItem(title))
            self.table.setItem(row_number, 1, QTableWidgetItem(year))
            self.table.setItem(row_number, 2, QTableWidgetItem(rating))
            self.table.setItem(row_number, 3, QTableWidgetItem(actor))


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()