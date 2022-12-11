import sqlite3
import util


class DatabaseAccess:
    def __init__(self, file: str):
        self.connection = sqlite3.connect(file, check_same_thread=False,
                                          detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS MicrosoftAccounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            password TEXT,
            points INT, 
            lastExec TIMESTAMP                               
        )
        """)
