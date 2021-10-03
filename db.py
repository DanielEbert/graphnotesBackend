import MySQLdb

class DB:
    def __init__(self, database="notes"):
        self.db = MySQLdb.connect(
            host="mysql",
            user="notesuser",
            passwd=PASSWD_SECRET,
            database=database,
            autocommit=True
        )

    def load(self, id: str):
        curs = self.db.cursor()
        curs.execute("SELECT data FROM notes WHERE id = %s", (id,))
        data = curs.fetchone()
        curs.close()
        if not data:
            return False, "No such Username"
        return True, data

    def save(self, id: str, data: str):
        # TODO: is there a try except maybe if sth doesnt work?
        curs = self.db.cursor()
        if not self.userExists(id):
            curs.execute("INSERT INTO notes (id, data) \
                          VALUES (%s, %s);", (id, data))
        else:
            curs.execute("UPDATE notes SET data = %s \
                          WHERE id = %s;", (data, id))
        curs.close()

    def userExists(self, id) -> bool:
        curs = self.db.cursor()
        curs.execute("SELECT 1 FROM notes WHERE id = %s;", (id,))
        userExists = curs.fetchone()
        curs.close()
        return True if userExists else False

    
