import datetime
import sqlite3

import database
import util


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d



class DatabaseConfig:
    def __init__(self, db_path: str = "./accounts.sqlite"):
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
        self.connection.commit()


if __name__ == '__main__':
    x = database.DatabaseAccess()
    # x.insert(
    #     util.MicrosoftAccount(
    #         email="ajksdlasddddj",
    #         password="aasddoisdjasd",
    #         lastExec=datetime.datetime.now(tz=datetime.timezone.utc)
    #     )
    # )
    x.delete(account=util.MicrosoftAccount(
        id='1', email='ajksdlasdj', password='this was updated', points=0,
        lastExec=datetime.datetime(2022, 12, 30, 19, 26, 2, 453184, tzinfo=datetime.timezone.utc)
    ))
