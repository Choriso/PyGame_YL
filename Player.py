import sqlite3
import os

class Player:
    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.score = 0

    def save_to_database(self):
        conn = sqlite3.connect('player_data.db')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                password TEXT NOT NULL,
                score INTEGER NOT NULL
            )
        ''')

        cursor.execute('SELECT * FROM players WHERE name=?', (self.name,))
        existing_player = cursor.fetchone()

        if existing_player:
            cursor.execute('''
                UPDATE players 
                SET password=?, score=?
                WHERE name=?
            ''', (self.password, self.score, self.name))
        else:
            cursor.execute('''
                INSERT INTO players (name, password, score)
                VALUES (?, ?, ?)
            ''', (self.name, self.password, self.score))

        conn.commit()
        conn.close()

    @classmethod
    def load_from_database(cls, name):
        conn = sqlite3.connect('player_data.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM players WHERE name=?', (name,))
        player_data = cursor.fetchone()

        conn.close()

        if player_data:
            return cls(name=player_data[1], password=player_data[2])

        return None

    @classmethod
    def get_all_players(cls):
        conn = sqlite3.connect('player_data.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM players')
        players_data = cursor.fetchall()

        conn.close()

        players_list = [cls(name=player[1], password=player[2]) for player in players_data]
        return players_list

    @classmethod
    def check_credentials(cls, name, password):
        conn = sqlite3.connect('player_data.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM players WHERE name=? AND password=?', (name, password))
        user_data = cursor.fetchone()

        conn.close()

        if user_data:
            return {"name": user_data[1], "score": user_data[3]}
        else:
            return None
