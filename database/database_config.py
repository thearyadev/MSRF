import sqlite3
import os
from pathlib import Path


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class DatabaseConfig:
    def __init__(self, db_path: str = "./accounts/accounts.sqlite"):
        if not os.path.exists(Path(db_path).parent): # in docker, this will be created when the volume is mounted
            os.makedirs(Path(db_path).parent)
            # but on the host, we need to create it
        
        self.connection = sqlite3.connect(db_path, check_same_thread=False)
        self.connection.row_factory = dict_factory
        self.cursor = self.connection.cursor()
        self.__init_table__()

    def __init_table__(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS MicrosoftAccount (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE,
                password TEXT,
                points INTEGER,
                lastExec TIMESTAMP
            )
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS PointCollectionHistory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pointsDelta INTEGER,
                sessionDuration INTEGER,
                accountName TEXT
            )
            """
        )

        self.connection.commit()
