from server_request import ServerRequest
from helpers import Helpers as Help
from sql_query import sql_query as sql
import json

class ServerRequest_AMSqlExplorer( ServerRequest ):

    def __init__(self):
        pass
    def post_request(self, page_request, query, data):
        """

        :param page_request:    page that is being requested
        :param query:           url query (after ?)
        :param data:            data that has been posted
        :return: (int [status], str [responce] )
        """

        response_data = self.new_response( 404, "Error: Not Found" )
        json_response = None

        if page_request == "/open_database":
            response_data = self.open_database(data)

        json_response = json.dumps(response_data)
        print(json_response)
        return json_response

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
        print(json_response)

        return json_response

    def open_database(self, database_name):
        """Opens database and responds with all table names"""
        if Help.file_exist(database_name):
            database = sql(database_name)
            data = database.get_all_tables()
            return self.new_response( 200, data )
        else:
            return self.new_response( 404, "Error: Database not found" )


