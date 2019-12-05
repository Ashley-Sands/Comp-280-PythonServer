from server_request import ServerRequest
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
        elif "table" in data and page_request == "/column_names":
            response_data = self.get_column_names(data["database"], data["table"])
        elif "table" in data and page_request == "/table_rows":
            response_data = self.get_all_table_rows(data["database"], data["table"])


        json_response = json.dumps(response_data)
        print("out data", json_response)
        #return response_data["status"], json_response
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

        return response_data["status"], json_response

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

    def get_column_names(self, database_name, table_name):

        # check the db and table exist
        if Help.file_exist(Config.get("db_root") + database_name):
            database = sql(database_name)
            if database.table_exist(table_name):
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
                return self.new_response(404, "Error: Table does not exist")
        else:
            return self.new_response(404, "Error: Database does not exist")

    def get_all_table_rows(self, db_name, table_name):

        if Help.file_exist(Config.get("db_root") + db_name):
            database = sql(db_name)
            if database.table_exist(table_name):
                data = database.select_from_table(table_name, "rowid, *")
                return self.new_response(200, data)
            else:
                return self.new_response(404, "Error: Table does not exist")
        else:
            return self.new_response(404, "Error: Database does not exist")
