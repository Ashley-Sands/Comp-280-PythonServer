from requestServers import server_request
import sql_query as sql
import json

class ServerRequest_Pacman( server_request.ServerRequest ):

    def __init__(self):

        # make sure that the database and required tables have been created
        self.database = sql.sql_query("pacman")

        # set up leader board
        lb_table_cols = ["username", "ghost_killed", "pills_collected", "level",
                         "time", "score", "level_mode", "data_submitted"]

        lb_col_data_types = ["VARCHAR", "INT", "INT", "INT", "FLOAT", "INT", "VARCHAR", "INT"]

        self.database.add_table("leaderboard", lb_table_cols, lb_col_data_types);

        pass

    def post_request(self, page_request, query, data):

        response_data = self.new_response( 404, "Error: Not Found" )
        json_response = None
        data = json.loads(data)

        return response_data["status"], response_data

    def get_request(self, page_request, query):

        response_data = self.new_response(404, "Error: Not Found")
        json_response = None

        return response_data["status"], response_data
