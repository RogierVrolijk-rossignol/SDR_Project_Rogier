"""
ASSIGNMENT ONE (TIC TAC TOE)
1. Shows the board of 9 fields, full width of the terminal.
2. Asks for next move.
3. Shows the board again.
4. Repeats until the game is over.

ASSIGNMENT TWO (SCREEN DUMP)
1. Makes a screenshot of a predefined region.
2. Uses coordinates: left_x, top_y, right_x, bottom_y.
3. Saves the screenshot as a .png file on the desktop.

ASSIGNMENT THREE
1. Gets the name of a specific window.
2. Finds that window.
3. Moves and resizes the window.
4. Makes a screenshot of that region.
"""

import os
import shutil
import sys
from pathlib import Path

import pyautogui
import pywinctl

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class TicTacToe:
    def __init__(self):
        self.board = [" "] * 9
        self.current_player = "X"

    def clear_screen(self):
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

    def show_board(self):
        width = shutil.get_terminal_size().columns
        line = "=" * width

        print(line)
        print("TIC TAC TOE".center(width))
        print(line)
        print()

        print(f" {self.board[0]} | {self.board[1]} | {self.board[2]} ".center(width))
        print("---+---+---".center(width))
        print(f" {self.board[3]} | {self.board[4]} | {self.board[5]} ".center(width))
        print("---+---+---".center(width))
        print(f" {self.board[6]} | {self.board[7]} | {self.board[8]} ".center(width))
        print()

        print("Positions:".center(width))
        print(" 1 | 2 | 3 ".center(width))
        print("---+---+---".center(width))
        print(" 4 | 5 | 6 ".center(width))
        print("---+---+---".center(width))
        print(" 7 | 8 | 9 ".center(width))
        print()

    def ask_move(self):
        while True:
            move = input(f"Player {self.current_player}, choose a field 1-9: ").strip()

            if not move.isdigit():
                print("Please enter a number.")
                continue

            move = int(move)

            if move < 1 or move > 9:
                print("Choose a number between 1 and 9.")
                continue

            index = move - 1

            if self.board[index] != " ":
                print("That field is already taken.")
                continue

            self.board[index] = self.current_player
            break

    def check_winner(self):
        winning_combinations = [
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),
            (0, 4, 8),
            (2, 4, 6),
        ]

        for a, b, c in winning_combinations:
            if self.board[a] == self.board[b] == self.board[c] and self.board[a] != " ":
                return self.board[a]

        if " " not in self.board:
            return "draw"

        return None

    def switch_player(self):
        if self.current_player == "X":
            self.current_player = "O"
        else:
            self.current_player = "X"

    def play(self):
        while True:
            self.clear_screen()
            self.show_board()

            result = self.check_winner()

            if result == "draw":
                print("Game over. It is a draw!")
                break

            if result == "X" or result == "O":
                print(f"Game over. Player {result} wins!")
                break

            self.ask_move()
            self.switch_player()


class ScreenDump:
    def __init__(self, left_x, top_y, right_x, bottom_y):
        self.left_x = left_x
        self.top_y = top_y
        self.right_x = right_x
        self.bottom_y = bottom_y

    def get_region(self):
        width = self.right_x - self.left_x
        height = self.bottom_y - self.top_y

        return self.left_x, self.top_y, width, height

    def make_screenshot(self, filename="screendump.png"):
        desktop = Path.home() / "Desktop"
        save_path = desktop / filename

        region = self.get_region()

        screenshot = pyautogui.screenshot(region=region)
        screenshot.save(save_path)

        return save_path


class WindowManager:
    def __init__(self, window_name):
        self.window_name = window_name

    def find_window(self):
        for window in pywinctl.getAllWindows():
            app_name = window.getAppName()
            title = window.title

            if self.window_name.lower() in app_name.lower() or self.window_name.lower() in title.lower():
                return window

        return None

    def move_and_resize_window(self, left_x, top_y, width, height):
        window = self.find_window()

        if window is None:
            return False

        window.moveTo(left_x, top_y)
        window.resizeTo(width, height)

        return True


def assignment_one():
    game = TicTacToe()
    game.play()


def assignment_two():
    screendump = ScreenDump(100, 100, 500, 500)
    save_path = screendump.make_screenshot("assignment_two_screendump.png")
    print("Screenshot saved to:", save_path)


def assignment_three(window_name):
    left_x = 100
    top_y = 100
    right_x = 500
    bottom_y = 500

    width = right_x - left_x
    height = bottom_y - top_y

    manager = WindowManager(window_name)
    window_found = manager.move_and_resize_window(left_x, top_y, width, height)

    if not window_found:
        return None

    screendump = ScreenDump(left_x, top_y, right_x, bottom_y)
    save_path = screendump.make_screenshot("assignment_three_window_screendump.png")

    return save_path


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Assignment App")
        self.setMinimumSize(QSize(500, 400))

        self.info_label = QLabel("Choose an assignment.")

        self.assignment_box = QComboBox()
        self.assignment_box.addItem("Assignment 1 - Tic Tac Toe")
        self.assignment_box.addItem("Assignment 2 - Screenshot region")
        self.assignment_box.addItem("Assignment 3 - Window screenshot")

        self.window_input = QLineEdit()
        self.window_input.setPlaceholderText("Window name, for example: Google Chrome")

        self.run_button = QPushButton("Run selected assignment")
        self.run_button.clicked.connect(self.run_assignment)

        self.window_list_button = QPushButton("Show open windows")
        self.window_list_button.clicked.connect(self.show_open_windows)

        self.result_list = QListWidget()

        layout = QVBoxLayout()
        layout.addWidget(self.info_label)
        layout.addWidget(self.assignment_box)
        layout.addWidget(self.window_input)
        layout.addWidget(self.run_button)
        layout.addWidget(self.window_list_button)
        layout.addWidget(self.result_list)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def run_assignment(self):
        selected_assignment = self.assignment_box.currentText()

        self.result_list.clear()

        if selected_assignment == "Assignment 1 - Tic Tac Toe":
            self.result_list.addItem("Tic Tac Toe starts in the terminal.")
            assignment_one()

        elif selected_assignment == "Assignment 2 - Screenshot region":
            screendump = ScreenDump(100, 100, 500, 500)
            save_path = screendump.make_screenshot("assignment_two_screendump.png")
            self.result_list.addItem(f"Screenshot saved to: {save_path}")

        elif selected_assignment == "Assignment 3 - Window screenshot":
            window_name = self.window_input.text().strip()

            if window_name == "":
                self.result_list.addItem("Please enter a window name first.")
                return

            save_path = assignment_three(window_name)

            if save_path is None:
                self.result_list.addItem("Window not found.")
            else:
                self.result_list.addItem(f"Window screenshot saved to: {save_path}")

    def show_open_windows(self):
        self.result_list.clear()

        for window in pywinctl.getAllWindows():
            app_name = window.getAppName()
            title = window.title

            self.result_list.addItem(f"{app_name} | {title}")


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()