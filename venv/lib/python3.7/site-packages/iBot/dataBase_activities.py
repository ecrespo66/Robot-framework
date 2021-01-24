import sqlite3


class Sqlite:
    def __init__(self, database):
        self.DataBase = database
        self.sqliteConnection = None
        self.cursor = None

    def __createConnection(self):
        self.sqliteConnection = sqlite3.connect(self.DataBase)
        self.cursor = self.sqliteConnection.cursor()

    def __closeConnection(self):
        self.sqliteConnection.commit()
        self.cursor.close()
        self.sqliteConnection.close()

    def tableList(self):
        tables = []
        try:
            self.__createConnection()
            self.cursor.execute('SELECT name from sqlite_master where type= "table"')
            TableList = self.cursor.fetchall()
            self.__closeConnection()
        except sqlite3.Error as error:
            raise error
        for table in TableList:
            tables.append(table[0])
        return tables

    def createTable(self, tableName, data):
        tables = self.tableList()
        if tableName not in tables:
            query = self.__createTableQuery(tableName, data)
            self.__createConnection()
            self.cursor.execute(query)
            self.__closeConnection()

    def Insert(self, tableName, data):
        try:
            self.createTable(tableName, data)
            InsertQuery = self.__insertQuery(tableName, data)
            self.__createConnection()
            self.cursor.execute(InsertQuery)
            self.__closeConnection()
        except sqlite3.Error as error:
            raise error

    def Query(self, query):
        try:
            self.__createConnection()
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            self.__closeConnection()
            return result
        except sqlite3.Error as error:
            raise error

    @staticmethod
    def __insertQuery(table_name, data):
        InsertQuery = "INSERT INTO " + table_name
        InsertQuery2 = ""
        FieldNames = ""
        QuestionMark = ""
        for x, y in data.items():
            FieldNames = FieldNames + str(x) + ", "
            QuestionMark = QuestionMark + "?, "
            InsertQuery2 = InsertQuery2 + "'" + str(y) + "', "
        QuestionMarks = "(" + (QuestionMark[:-1])[:-1] + "), "
        FieldNames = " (" + (FieldNames[:-1])[:-1] + ")"
        InsertQuery = (InsertQuery + FieldNames + " VALUES " + "(" + InsertQuery2[:-1])[:-1] + ");"
        return InsertQuery

    @staticmethod
    def __createTableQuery(table_name, data, types=None):
        if types is None:
            types = {}
        for x, y in data.items():
            if str(type(y)) == "<class 'str'>":
                tipo = "TEXT"
                types[x] = tipo

            elif str(type(y)) == "<class 'int'>":
                tipo = "NUMERIC"
                types[x] = tipo

        dict = [types, data]
        query = "CREATE TABLE " + table_name + " ("
        query2 = ""

        for row in dict:
            if dict.index(row) == 0:
                for x, y in row.items():
                    query2 = query2 + x + " " + y + ", "
        query = query + (query2[:-1])[:-1] + ")"
        return query
