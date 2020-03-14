from requestServers import server_request
import sql_query as sql

class TEST_mysql( server_request.ServerRequest  ):

    def __init__( self ):

        # connect to data
        self.database = sql.sql_query("py_test", using_mysql=True)
        #self.database.connect_db()

        tables = self.database.get_all_tables()

        # destroy and close
        #self.database.destroy_database()
        #self.database.close_db()

        print(tables)
