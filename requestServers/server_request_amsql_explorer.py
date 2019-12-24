from requestServers.server_request import ServerRequest
from helpers import Helpers as Help
from sql_query import sql_query as sql
import json
from Globals import GlobalConfig as Config

class ServerRequest_AMSqlExplorer( ServerRequest ):

    def __init__(self):
        # make sure that the db root is set
        if not Config.is_set("db_root"):
            Config.set("db_root", "")

    def post_request(self, page_request, query, data):
        """

        :param page_request:    page that is being requested
        :param query:           url query (after ?)
        :param data:            data that has been posted (as jason string)
        :return: (int [status], str [responce] )
        """

        print(page_request)
        response_data = self.new_response( 404, "Error: Not Found" )
        json_response = None
        data = json.loads(data)
        print("in data", data)

        print("table" in data)

        if page_request == "/open_database":
            response_data = self.open_database(data["database"])
        elif page_request == "/new_database":
            response_data = self.new_database(data["database"])
        elif page_request == "/table_exist" and Help.check_keys(data, ["table"]):
            response_data = self.database_and_table_exist(data["database"], data["table"])
        elif page_request == "/table_not_exist" and Help.check_keys(data, ["table"]):
            response_data = self.table_does_not_exist(data["database"], data["table"])
        elif page_request == "/column_names" and Help.check_keys(data, ["table"]) :
            response_data = self.get_column_names(data["database"], data["table"])
        elif page_request == "/table_rows" and Help.check_keys(data, ["table"]) :
            response_data = self.get_all_table_rows(data["database"], data["table"])
        elif page_request == "/drop_table" and Help.check_keys(data, ["table"]):
            response_data = self.drop_table( data["database"], data["table"] )
        elif page_request == "/update_row" and Help.check_keys(data, ["table", "set_columns", "set_data", "where_columns", "where_data"]):
            response_data = self.update_row(data["database"], data["table"], data["set_columns"], data["set_data"], data["where_columns"], data["where_data"])
        elif page_request == "/remove_row" and Help.check_keys(data, ["table", "where_columns", "where_data"]):
            response_data = self.remove_row_from_table(data["database"], data["table"], data["where_columns"], data["where_data"])
        elif page_request == "/insert_row" and Help.check_keys(data, ["table", "value_columns", "value_data"]):
            response_data = self.insert_row(data["database"], data["table"], data["value_columns"], data["value_data"])
        elif page_request == "/new_table" and Help.check_keys(data, ["table", "column_names", "data_types", "data_lengths", "default_values"]):
            response_data = self.new_table(data["database"], data["table"], data["column_names"], data["data_types"], data["data_lengths"], data["default_values"])

        print(response_data)
        json_response = json.dumps(response_data)
        print("out data", json_response)

        return 200, json_response

    def get_request(self, page_request, query):
        """

        :param page_request:    page that is being requested
        :param query:           url query (after ?)
        :return: (int [status], str [responce] )
        """

        response_data = self.new_response(404, "Error: Not Found")
        json_response = None

        if page_request == "/open_database":
            response_data = self.open_database(query)

        json_response = json.dumps(response_data)
        print(json_response, query)

        return 200, json_response

    def get_database(self, db_name, table_name):
        """ gets the database if tables exists in database,

        :param db_name:     name of database to check
        :param table_name:  name of table to find in database
        :return:            instance of database, or error response
        """

        if Help.file_exist(Config.get("db_root") + db_name):
            database = sql(db_name)
            if database.table_exist(table_name):
                return database
            else:
                return self.new_response(404, "Error: Table does not exist")
        else:
            return self.new_response(404, "Error: Database does not exist")

    def database_and_table_exist(self, db_name, table_name):

        database = self.get_database(db_name, table_name)

        if type(database) is sql:
            return self.new_response(200, "success")
        else:
            return database

    def table_does_not_exist(self, db_name, table_name):
        """ Checks that table does not exist in database"""

        if Help.file_exist(Config.get("db_root") + db_name):
            database = sql(db_name)
            if not database.table_exist(table_name):
                return self.new_response(200, "success")
            else:
                return self.new_response(404, "Error: Table does exist")
        else:
            return self.new_response(404, "Error: Database does not exist")

    def open_database(self, database_name):
        """Opens database and responds with all table names"""
        if Help.file_exist(Config.get("db_root") + database_name):
            database = sql(database_name)
            data = database.get_all_tables()
            return self.new_response( 200, data )
        else:
            return self.new_response( 404, "Error: Database not found" )

    def new_database(self, database_name):

        if not Help.file_exist(Config.get("db_root") + database_name):
            database = sql(database_name)
            database.connect_db()
            database.close_db()
            return self.new_response(200, "Success")
        else:
            return self.new_response(404, "Error: Already Exist")

    def new_table(self, database_name, new_table_name, column_names, data_types, data_lengths, default_values):

        if Help.file_exist(Config.get("db_root") + database_name):
            database = sql(database_name)

            response = database.add_table(new_table_name, column_names, data_types, data_lengths, default_values)

            if response is None:
                return self.new_response(200, "success")
            else:
                return self.new_response(response[0], response[1])
        else:
            return self.new_response(404, "Error: Database does not exist")

    def get_column_names(self, db_name, table_name):

        # check the db and table exist
        database = self.get_database(db_name, table_name)

        if type(database) is sql:
            # get all the column names
            data = database.get_table_columns(table_name)

            # add the editable value to the end of each row
            for i in range(len(data)):
                data[i] = list(data[i])
                data[i].append(1)

            # add the rowid column to the data (default column in sqlite)
            data = [[-1, "rowid", "INT", 0, None, 1, 0], *data]

            return self.new_response(200, data)
        else:
            return database

    def get_all_table_rows(self, db_name, table_name):

        database = self.get_database(db_name, table_name)

        if type(database) is sql:
            data = database.select_from_table(table_name, ["rowid", "*"])
            return self.new_response(200, data)
        else:
            return database

    def update_row(self, db_name, table_name, set_columns, set_data, where_columns, where_data):
        """

        :param db_name:         name of database
        :param table_name:      name of table to update
        :param set_columns:     list of column names to be updated
        :param set_data:        list of data (must match set_columns)
        :param where_columns:   list of where columns
        :param where_data:      list of where data (must match where_columns)
        :return:                returns status
        """
        database = self.get_database(db_name, table_name)

        if type(database) is sql:
            database.update_row(table_name, set_columns, set_data, where_columns, where_data)
            return self.new_response(200, "success")
        else:
            return database

    def insert_row(self, db_name, table_name, value_columns, value_data):
        database = self.get_database(db_name, table_name)

        if type(database) is sql:
            database.insert_row(table_name, value_columns, value_data)
            return self.new_response(200, "success")
        else:
            return database

    def drop_table(self, db_name, table_name):
        database = self.get_database(db_name, table_name)

        if type(database) is sql:
            database.drop_table( table_name )
            return self.new_response(200, "success")
        else:
            return database

    def remove_row_from_table(self, db_name, table_name, where_columns, where_data):

        database = self.get_database(db_name, table_name)

        if type(database) is sql:
            database.remove_row(table_name, where_columns, where_data)
            return self.new_response(200, "success")
        else:
            return database