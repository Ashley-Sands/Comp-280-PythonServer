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
        print(data)

        if page_request == "/open_database":
            response_data = self.open_database(data["database"])
        elif page_request == "/new_database":
            response_data = self.new_database(data["database"])
        elif "table" in data and page_request == "/column_names":
            responce_data = self.get_column_names(data["database"], data["table"])


        json_response = json.dumps(response_data)
        print(json_response)
        return response_data["status"], json_response

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

