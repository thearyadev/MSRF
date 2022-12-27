import database
import util
import typing
import datetime


class DatabaseAccess(database.DatabaseConfig):
    def __init__(self, url):
        super().__init__(url=url)
        self._dt_format = "%Y-%m-%d %H:%M:%S"

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


if __name__ == '__main__':
    x = DatabaseAccess("http://localhost:8090")
    a = x.read()[0]
    a.points = 5000
    x.write(a)
