import database
import util

import threading

lock = threading.Lock()


class DatabaseAccess(database.DatabaseConfig):
    def __init__(self, db_path: str = "./accounts.sqlite"):
        super().__init__(db_path)

    def insert(self, account: util.MicrosoftAccount):
        self.cursor.execute(
            """
            INSERT INTO MicrosoftAccount (email, password, lastExec, points) VALUES (?, ?, ?, ?)
            """,
            (account.email, account.password, account.lastExec, account.points)
        )
        self.connection.commit()

    def read(self) -> list[util.MicrosoftAccount]:
        self.cursor.execute(
            """
            SELECT * FROM MicrosoftAccount
            """
        )
        return [util.MicrosoftAccount(**data) for data in self.cursor.fetchall()]

    def write(self, account: util.MicrosoftAccount):
        self.cursor.execute(
            """
            UPDATE MicrosoftAccount
            SET email = ?, password = ?, lastExec = ?, points = ?
            WHERE id = ?
            """,
            (account.email, account.password, account.lastExec, account.points, account.id)
        )
        self.connection.commit()

    def delete(self, account: util.MicrosoftAccount):
        self.cursor.execute(
            """
            DELETE FROM MicrosoftAccount
            WHERE id = ?
            """,
            (account.id,)
        )
        self.connection.commit()
