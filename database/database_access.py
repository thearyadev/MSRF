import database
import util

import threading

lock = threading.Lock()


class DatabaseAccess(database.DatabaseConfig):
    def __init__(self, db_path: str = "./accounts.sqlite"):
        super().__init__(db_path)

    def insert(self, account: util.MicrosoftAccount):
        lock.acquire()
        self.cursor.execute(
            """
            INSERT INTO MicrosoftAccount (email, password, lastExec, points) VALUES (?, ?, ?, ?)
            """,
            (account.email, account.password, account.lastExec, account.points)
        )
        self.connection.commit()
        lock.release()

    def read(self) -> list[util.MicrosoftAccount]:
        lock.acquire()
        self.cursor.execute(
            """
            SELECT * FROM MicrosoftAccount
            """
        )
        data = [util.MicrosoftAccount(**data) for data in self.cursor.fetchall()]
        lock.release()
        return data

    def write(self, account: util.MicrosoftAccount):
        lock.acquire()
        self.cursor.execute(
            """
            UPDATE MicrosoftAccount
            SET email = ?, password = ?, lastExec = ?, points = ?
            WHERE id = ?
            """,
            (account.email, account.password, account.lastExec, account.points, account.id)
        )
        self.connection.commit()
        lock.release()

    def delete(self, account: util.MicrosoftAccount):
        lock.acquire()
        self.cursor.execute(
            """
            DELETE FROM MicrosoftAccount
            WHERE id = ?
            """,
            (account.id,)
        )
        self.connection.commit()
        lock.release()
