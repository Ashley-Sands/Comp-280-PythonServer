from requestServers import server_request
import sql_query as sql

class TEST_mysql( server_request.ServerRequest  ):

    def __init__( self ):

        # connect to data
        self.database = sql.sql_query("py_test", using_mysql=True)
        self.litedb = sql.sql_query("pytest")

        #self.database.connect_db()

        tables = self.database.get_all_tables()
        cols = self.database.get_table_columns("test")

        self.litedb.add_table("test_lite", ["a", "b"], ["INT", "INT"])
        self.litedb.add_table("test_lite2", ["a", "b"], ["INT", "INT"])
        tables_lite = self.litedb.get_all_tables()
        cols_lite = self.litedb.get_table_columns("test_lite")

        # destroy and close
        #self.database.destroy_database()
        #self.database.close_db()

        print(tables, cols)
        print("lite:", tables_lite, cols_lite)
