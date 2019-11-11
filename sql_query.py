import sqlite3
from Globals import Global

class sql_query():

    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def connect_db(self):
        # connect to the DB to check it exist and close the connect so other application can use the db.
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def close_db(self, commit = True):
        if commit:
            self.connection.commit()
        self.connection.close()

    def table_exist(self, table_name, close_connect = True):

        query = "SELECT name FROM sqlite_master WHERE type='table' AND name=? "

        self.connect_db()

        self.cursor.execute(query, (table_name,))
        row_count = len( self.cursor.fetchall() )

        if close_connect:
            self.close_db()

        return row_count

    ''' Check if table exist else creats it.
    @:param table_name: Name of the table to be created.
    @:param col_names: col string
    '''
    def add_table(self, table_name, col_names):

        if self.table_exist( table_name ):
            print("Error: can not create table, already exist")
            return

        self.connect_db()

        query = "CREATE TABLE "+table_name+" ("+col_names+")"
        self.cursor.execute(query)

        self.close_db()

        print("Table Created")

    def insert_row(self, table_name, col_names, row_data):

        if not self.table_exist(table_name):
            print("Error: can not insert row into table, table does not exist")
            return

        self.connect_db()

        col_name_str = ', '.join( col_names )
        col_value_str = ', '.join( ["?"] * len(row_data) )

        query = "INSERT INTO " + table_name + " (" + col_name_str + ") VALUES (" + col_value_str + ") "
        if Global.DEBUG:
            print("query: ", query, "Data", row_data)
        self.cursor.execute( query, row_data )

        self.close_db()

        print("data Inserted to table")

    def remove_row(self, table_name, where_str, where_data):

        if not self.table_exist(table_name):
            print("Error: can not delete row from table, table does not exist")
            return

        self.connect_db()

        query = " DELETE FROM "+table_name+" WHERE "+where_str

        if Global.DEBUG:
            print(query, where_data)

        self.cursor.execute( query, where_data )

        self.close_db()

    def select_from_table(self, table_name, cols_str, where_str, where_data =""):

        if not self.table_exist(table_name):
            print("Error: can not select from table, table does not exist")
            return

        self.connect_db()

        if len(where_str) > 0:
            where_str = " WHERE "+where_str
        else:
            where_str = ""

        query = "SELECT " + cols_str + " FROM " + table_name + where_str

        self.cursor.execute( query, where_data )
        data = self.cursor.fetchall()

        self.close_db()

        return data

    def update_row(self, table_name, set_str, where_str, where_data ):

        if not self.table_exist(table_name):
            print("Error: can not update row in table, table does not exist")
            return

        self.connect_db()

        query = "UPDATE "+table_name+" SET "+set_str+" WHERE "+where_str

        print( query )

        self.cursor.execute(query, where_data)

        self.close_db()
