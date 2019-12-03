
import sql_query
import json


class ServerRequest:

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

    def new_response(self, status, response):
        """Creates a new response read for json convert
        :param status:      status code ie 200 or 404
        :param response:    the responce data
        :return:            a dict of response data {status, response}
        """
        response_dict = {}
        response_dict["status"] = status
        response_dict["response"] = response

        return response_dict

