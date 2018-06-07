import sqlite3,os

class DbOperator:
    def __init__(self):
        dbname = 'malformedurls.db'
        path = os.getcwd()
        self.dbpath = os.path.join(path,dbname)
        if os.path.exists(self.dbpath):
            self.connector()


    def connector(self):
        self.con = sqlite3.connect(self.dbpath)
        self.cur = self.con.cursor()

    def tableCreator(self):
        query = "CREATE TABLE IF NOT EXISTS urls (id INTEGER PRIMARY KEY AUTOINCREMENT,url TEXT,checked INT DEFAULT 0,status_code TEXT,urlType text)"
        self.cur.execute(query)
        self.con.commit()

    def isChecked(self,url):
        query = "SELECT CHECKED FROM urls WHERE url='{}' LIMIT 0,1".format(url)
        q = self.cur.execute(query).fetchone()

        if q == 1:
            return True
        else:
            return False

    def isAdded(self,url):
        query = "SELECT url FROM urls WHERE url='{}' LIMIT 0,1".format(url)
        q = self.cur.execute(query).fetchone()

        if q == None:
            return True
        else:
            return False

    def urlAdd(self,url):
        query = "INSERT INTO urls(url) VALUES('{}')".format(url)

        self.cur.execute(query)
        self.con.commit()

    def dbCheck(self):
        if os.path.exists(self.dbpath) == True:
            return True
        else:
            return False

    def dbCount(self):
        query = "SELECT seq FROM sqlite_sequence"
        q = self.cur.execute(query)
        return q.fetchone()[0]

    def returnItem(self,id):
        query = "SELECT url FROM urls WHERE id='{}' and CHECKED='0'".format(id)

        q= self.cur.execute(query)
        try:
            return q.fetchone()[0]
        except TypeError:
            return False

    def urlChecked(self,url,status_code):
        query = "UPDATE urls SET CHECKED=1,status_code='{}' WHERE url='{}'".format(status_code,url)
        self.cur.execute(query)
        self.con.commit()

    def getAll(self):
        query = "SELECT url,status_code FROM urls WHERE CHECKED=1"
        q = self.cur.execute(query).fetchall()
        return q