from requestServers import server_request
import sql_query as sql
import json
from helpers import Helpers as Help

class ServerRequest_Pacman( server_request.ServerRequest ):



    def __init__(self):

        # make sure that the database and required tables have been created
        self.database = sql.sql_query("pacman")

        # set up leader board
        lb_table_cols = ["username", "ghost_killed", "pills_collected", "level",
                         "time", "score", "level_mode", "date_submitted"]

        lb_col_data_types = ["VARCHAR", "INT", "INT", "INT", "FLOAT", "INT", "VARCHAR", "INT"]

        self.database.add_table("leaderboard", lb_table_cols, lb_col_data_types);

    def post_request(self, page_request, query, data):

        response_data = self.new_response( 404, "Error: Not Found" )
        json_response = None
        data = json.loads(data)

        if page_request == "/submit_score" and \
                Help.check_keys(data, self.database.get_table_column_names("leaderboard")):  # insure all data is provided
            pass

        print(data)

        return self.parse_response(response_data)

    def get_request(self, page_request, query):

        response_data = self.new_response(404, "Error: Not Found")
        json_response = None

        return self.parse_response(response_data)
