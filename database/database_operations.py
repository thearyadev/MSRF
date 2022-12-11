import util
import database


class DatabaseOperations(database.DatabaseAccess):
    def __init__(self, file):
        super().__init__(file=file)

    def get_all(self) -> list[util.MicrosoftAccount]:
        self.cursor.execute("SELECT * FROM MicrosoftAccounts")
        accounts: list[util.MicrosoftAccount] = list()
        for accountEntry in self.cursor.fetchall():
            accounts.append(
                util.MicrosoftAccount(
                    id=accountEntry[0],
                    email=accountEntry[1],
                    password=accountEntry[2],
                    points=accountEntry[3],
                    lastExecution=accountEntry[4]
                )
            )

        return accounts

    def insert(self, account: util.MicrosoftAccount) -> bool:
        self.cursor.execute(f"""
         INSERT INTO MicrosoftAccounts(email, password, points, lastExec)
         VALUES(?, ?, ?, ?)
         """, (account.email, account.password, account.points, account.lastExecution))
        self.connection.commit()
        return True

if __name__ == '__main__':
    x = DatabaseOperations(file="../accounts.db")
    print(x.get_all())