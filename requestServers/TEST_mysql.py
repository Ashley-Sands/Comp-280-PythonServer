from requestServers import server_request
import sql_query as sql

class TEST_mysql( server_request.ServerRequest  ):

    def __init__( self ):

        self.database = sql.sql_query("py_test", using_mysql=True)
        self.database.connect_db()
        self.database.destroy_database()
