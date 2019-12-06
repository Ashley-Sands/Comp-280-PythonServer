import sqlite3
from Globals import Global
from Globals import GlobalConfig as Config

class sql_query():

    def __init__(self, db_name):

        # make sure that the db root is set
        if not Config.is_set( "db_root" ):
            Config.set("db_root", "")

        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def connect_db(self):
        """ Connect to the SQLite DB, creates new if not exist """
        self.connection = sqlite3.connect(Config.get("db_root")+self.db_name)
        self.cursor = self.connection.cursor()

    def close_db(self, commit = True):
        """Closes the db connection"""
        if commit:
            self.connection.commit()
        self.connection.close()

    def get_all_tables(self):
        """ Gets an list of tuples with all table names in database

        :return: list of table names [table_name, ...]
        """
        query = "SELECT name FROM sqlite_master WHERE type='table'"

        self.connect_db()

        self.cursor.execute(query)
        data = self.cursor.fetchall()

        # clean the data removing the inner list of 1 element
        for i in range (len(data)):
            data[i] = data[i][0]

        self.close_db()

        return data

    def get_table_columns(self, table_name):
        """ Gets a list of tuples with all column data for table

        :param table_name:  table to get column data from
        :return:            [(col_id, col_name, type, can_be_null, default_value, part_of_primary_key)...]
        """
        query = "pragma table_info("+table_name+")"

        self.connect_db()

        self.cursor.execute(query)
        data = self.cursor.fetchall()
        row_count = len(data)

        print(row_count, data)

        self.close_db()

        return data

    def table_exist(self, table_name, close_connect = True):
        """Check if table exist in database"""
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
        """Adds new table to database"""
        if self.table_exist( table_name ):
            print("Error: can not create table, already exist")
            return

        self.connect_db()

        query = "CREATE TABLE "+table_name+" ("+col_names+")"
        self.cursor.execute(query)

        self.close_db()

        print("Table Created")

    def drop_table(self, table_name):
        """drops table from database"""
        if not self.table_exist( table_name ):
            print("Error: can not drop table, that does not already exist")
            return

        self.connect_db()

        query = "DROP TABLE " + table_name
        self.cursor.execute(query)

        self.close_db()

    def insert_row(self, table_name, col_names, row_data):
        """Inserts rot into table"""
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
        """removerow from table"""
        if not self.table_exist(table_name):
            print("Error: can not delete row from table, table does not exist")
            return

        self.connect_db()

        query = " DELETE FROM "+table_name+" WHERE "+where_str

        if Global.DEBUG:
            print(query, where_data)

        self.cursor.execute( query, where_data )

        self.close_db()

    def select_from_table(self, table_name, cols_str, where_str="", where_data =""):
        """Selects rows of data from table"""
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

    def update_row(self, table_name, set_columns, set_data, where_columns, where_data ):
        """ Updates table row

        :param table_name:      Name of table to update
        :param set_columns:     list or tuple of columns to set
        :param set_data:        list or tuple of data to set into columns (order must match set_str)
        :param where_columns:   list or tuple of wheres
        :param where_data:      list or tuple of where data (order must match where_str)
        :return:
        """
        if not self.table_exist(table_name):
            print("Error: can not update row in table, table does not exist")
            return

        set_str = self.sql_string_builder(set_columns, ",")
        where_str = self.sql_string_builder(where_columns, "AND ")
        data = (*set_data, *where_data)

        self.connect_db()

        query = "UPDATE "+table_name+" SET "+set_str+" WHERE "+where_str

        print( query )

        self.cursor.execute(query, data)

        self.close_db()

    def sql_string_builder(self, column_names, join):
        """ build a list of column names in to sql query string for set and where ect... """

        str = ""

        # make column string
        for s in column_names:
            str += s + "=? "+join

        # clear end ','
        if str[-len(join):] == ",":
            set_str = str[:-len(join)]

        return str

if __name__ == "__main__":

    sql = sql_query("databases/test_db")

    while(1):
        inp = input()
        inp = inp.lower()
        inp = inp.split(":")
        print(inp)
        if inp[0] == "exit":
            exit()
        elif inp[0] == "drop":
            sql.drop_table(inp[1])
            print("Droped")
