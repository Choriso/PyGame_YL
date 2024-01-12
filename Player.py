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

        # Создаем таблицу, если ее нет
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                password TEXT NOT NULL,
                score INTEGER NOT NULL
            )
        ''')

        # Проверяем, есть ли уже такой игрок в базе
        cursor.execute('SELECT * FROM players WHERE name=?', (self.name,))
        existing_player = cursor.fetchone()

        if existing_player:
            # Если игрок уже существует, обновляем его данные
            cursor.execute('''
                UPDATE players 
                SET password=?, score=?
                WHERE name=?
            ''', (self.password, self.score, self.name))
        else:
            # Иначе создаем новую запись
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
            # Возвращаем экземпляр класса Player с загруженными данными
            return cls(name=player_data[1], password=player_data[2])

        return None
