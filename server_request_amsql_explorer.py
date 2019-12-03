from server_request import ServerRequest
from sql_query import sql_query as sql

class ServerRequest_AMSqlExplorer( ServerRequest ):

    def post_request(self, page_request, query, data):
        """

        :param page_request:    page that is being requested
        :param query:           url query (after ?)
        :param data:            data that has been posted
        :return: (int [status], str [responce] )
        """
        return 404, "Error: Not Found"

    def get_request(self, page_request, query):
        """

        :param page_request:    page that is being requested
        :param query:           url query (after ?)
        :return: (int [status], str [responce] )
        """
        return 404, "Error: Not Found"