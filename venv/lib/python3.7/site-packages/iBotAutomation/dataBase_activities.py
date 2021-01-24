# llama a la funcion "SqliteInsert(DataBase, table_name , diccionary, **kwargs)"
import sqlite3


class Sqlite:
    def __init__(self, database):
        self.cursor = self.sqliteConnection.cursor()
        self.sqliteConnection = sqlite3.connect(self.DataBase)
        self.DataBase = database
        self.Tables = self.Query('SELECT name from sqlite_master where type= "table"')
        self.createConexion()

    @staticmethod
    def insertData(table_name, data):
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
    def createTable(table_name, data, types=None):
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

    def Insert(self, table_name, data):
        try:
            self.cursor.execute('SELECT name from sqlite_master where type= "table"')
            TableList = self.cursor.fetchall()
            Tables = []
            for table in TableList:
                Tables.append(table[0])

            if table_name not in Tables:
                QueryTable = self.createTable(table_name, data)
                self.cursor.execute(QueryTable)

        except sqlite3.Error as error:
            return error

        try:
            InsertQuery = self.insertData(table_name, data)
            self.cursor.execute(InsertQuery)
            self.sqliteConnection.commit()
            self.cursor.close()

        except sqlite3.Error as error:
            return error
        finally:
            if self.sqliteConnection:
                self.cursor.close()
                self.sqliteConnection.close()

    def Query(self, query):
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            self.sqliteConnection.commit()
            self.cursor.close()
            self.sqliteConnection.close()
            return result
        except sqlite3.Error as error:
            return error
