import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QComboBox
import mysql.connector

class GameInventoryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Game Inventory Management')

        layout = QVBoxLayout()

        # Add game form
        form_layout = QHBoxLayout()
        self.name_input = QLineEdit(self)
        self.genre_combobox = QComboBox(self)
        self.genre_combobox.addItems(["Action", "FPS", "RPG", "Strategy", "Simulation", "Sports", "Other"])
        self.platform_combobox = QComboBox(self)
        self.platform_combobox.addItems(["PC", "PS5", "Xbox", "Nintendo", "Mobile", "Other"])
        form_layout.addWidget(QLabel('Name:'))
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(QLabel('Genre:'))
        form_layout.addWidget(self.genre_combobox)
        form_layout.addWidget(QLabel('Platform:'))
        form_layout.addWidget(self.platform_combobox)
        self.add_btn = QPushButton('Add Game', self)
        self.add_btn.clicked.connect(self.add_game)
        form_layout.addWidget(self.add_btn)
        layout.addLayout(form_layout)

        # Game inventory table
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['ID', 'Name', 'Genre', 'Platform'])
        layout.addWidget(self.table)

        # Remove game form
        remove_layout = QHBoxLayout()
        self.remove_id_input = QLineEdit(self)
        remove_layout.addWidget(QLabel('Game ID to Remove:'))
        remove_layout.addWidget(self.remove_id_input)
        self.remove_btn = QPushButton('Remove Game', self)
        self.remove_btn.clicked.connect(self.remove_game)
        remove_layout.addWidget(self.remove_btn)
        layout.addLayout(remove_layout)

        self.setLayout(layout)
        self.load_games()

    def connect_db(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="asqo-140",  
            database="game_inventory"
        )

    def add_game(self):
        name = self.name_input.text()
        genre = self.genre_combobox.currentText()
        platform = self.platform_combobox.currentText()
        if name and genre and platform:
            db = self.connect_db()
            cursor = db.cursor()
            cursor.execute("INSERT INTO games (name, genre, platform) VALUES (%s, %s, %s)", (name, genre, platform))
            db.commit()
            db.close()
            self.load_games()
            QMessageBox.information(self, 'Success', 'Game added successfully!')
        else:
            QMessageBox.warning(self, 'Error', 'Please fill in all fields.')

    def load_games(self):
        db = self.connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM games")
        games = cursor.fetchall()
        db.close()

        self.table.setRowCount(len(games))
        for row_num, game in enumerate(games):
            self.table.setItem(row_num, 0, QTableWidgetItem(str(game[0])))
            self.table.setItem(row_num, 1, QTableWidgetItem(game[1]))
            self.table.setItem(row_num, 2, QTableWidgetItem(game[2]))
            self.table.setItem(row_num, 3, QTableWidgetItem(game[3]))

    def remove_game(self):
        game_id = self.remove_id_input.text()
        if game_id:
            db = self.connect_db()
            cursor = db.cursor()
            cursor.execute("DELETE FROM games WHERE id = %s", (game_id,))
            db.commit()
            db.close()
            self.load_games()
            QMessageBox.information(self, 'Success', 'Game removed successfully!')
        else:
            QMessageBox.warning(self, 'Error', 'Please enter a game ID.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GameInventoryApp()
    ex.show()
    sys.exit(app.exec_())
def add_game(self):
    name = self.name_input.text()
    genre = self.genre_combobox.currentText()
    platform = self.platform_combobox.currentText()
    if name and genre and platform:
        db = self.connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM games WHERE name = %s", (name,))
        result = cursor.fetchone()
        if result[0] > 0:
            QMessageBox.warning(self, 'Error', 'This game is already added.')
        else:
            cursor.execute("INSERT INTO games (name, genre, platform) VALUES (%s, %s, %s)", (name, genre, platform))
            db.commit()
            db.close()
            self.load_games()
            QMessageBox.information(self, 'Success', 'Game added successfully!')
    else:
        QMessageBox.warning(self, 'Error', 'Please fill in all fields.')