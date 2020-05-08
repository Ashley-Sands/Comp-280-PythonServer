import requestServers.server_request as server_request
import json

class ServerWebhookTrigger( server_request.ServerRequest ):

    def get_request(self, page_request, query):
        """

        :param page_request:    page that is being requested
        :param query:           url query dict of query data (key=value)
        :return: (int [status], str [responce] )
        """
        if page_request == "/commit":
            return 200, "Helloooo World"
        else:
            return 404, ""
