import database
import util
import typing
import datetime
from util import deprecated





@deprecated
class DatabaseAccessLegacy(database.DatabaseConfigLegacy):
    def __init__(self, url):
        super().__init__(url=url)
        self._dt_format = "%Y-%m-%d %H:%M:%S"

    def insert(self, account: util.MicrosoftAccount):
        accountData = account.dict()
        accountData["lastExec"] = account.lastExec.strftime(self._dt_format)
        self.records.create("microsoft_account", body_params=accountData)

    def delete(self, account):
        self.records.delete("microsoft_account", account.id)

    def write(self, account: util.MicrosoftAccount):
        accountData = account.dict()
        accountData["lastExec"] = account.lastExec.strftime(self._dt_format)

        self.records.update("microsoft_account", account.id, body_params=accountData)

    def read(self) -> list[util.MicrosoftAccount]:
        accountsAsRecord: list[util.MicrosoftAccount] | typing.Any = self.records.get_full_list("microsoft_account")
        accounts: list[util.MicrosoftAccount] = list()

        for a in accountsAsRecord:
            accounts.append(
                util.MicrosoftAccount(
                    id=a.id,
                    email=a.email,
                    password=a.password,
                    lastExec=a.last_exec,
                    points=a.points
                )
            )
        return accounts


class DatabaseAccess(database.DatabaseConfig):
    def __init__(self, db_path: str = "./accounts.sqlite"):
        super().__init__(db_path)

    def insert(self, account: util.MicrosoftAccount):
        self.cursor.execute(
            """
            INSERT INTO MicrosoftAccount (email, password, lastExec) VALUES (?, ?, ?)
            """,
            (account.email, account.password, account.lastExec)
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
            SET email = ?, password = ?, lastExec = ?
            WHERE id = ?
            """,
            (account.email, account.password, account.lastExec, account.id)
        )
        self.connection.commit()

    def delete(self, account: util.MicrosoftAccount):
        self.cursor.execute(
            """
            DELETE FROM MicrosoftAccount
            WHERE id = ?
            """,
            (account.id, )
        )
        self.connection.commit()