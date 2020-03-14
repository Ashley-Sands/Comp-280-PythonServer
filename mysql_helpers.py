import random

class MySqlHelpers:
    import mysql.connector as MYSQL
    import mysql.connector.errorcode as MYSQL_ERROR

    @staticmethod
    def mysql_connect( host, user, passwd, db_name ):
        """ The is to mimic the sqlite3.connect function with the addison of returning the cursor as well
        so if the db does not exist it is created!
        :return: the connection to the database, and the cursor. None if error
        """
        # check that we can connect to the database.
        db_connection = None
        db_cursor = None
        print("mysql details: ", host, user, "*"*random.randint(6, 16), db_name)
        try:
            db_connection = MySqlHelpers.MYSQL.connect( host=host, user=user, passwd=passwd)
            db_cursor = db_connection.cursor()
            print( "mysql: Connected" )
        except Exception as err:
            print("mysql ERROR: ", err)
            return None

        # select the database otherwise create it!
        try:
            db_cursor.execute("USE "+db_name)
        except:
            print("mysql: Creating new database,", db_name)
            db_cursor.execute( "CREATE DATABASE " + db_name )
            db_cursor.execute("USE "+db_name)

        print("mysql: database", db_name, "selected")

        return db_connection, db_cursor
