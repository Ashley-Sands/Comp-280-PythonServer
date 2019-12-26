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
                response_data = self.submit_score(data)

        return self.parse_response(response_data)

    def get_request(self, page_request, query):

        response_data = self.new_response(404, "Error: Not Found")
        json_response = None

        if page_request == "/leaderboard" and "game_mode" in query:
            response_data = self.get_scores(query["game_mode"])

        return self.parse_response(response_data)

    def submit_score(self, data):

        col_names = self.database.get_table_column_names("leaderboard")
        col_values = []
        # since we have checked that the data exist we can just loop through all the column names
        # and just append the values so they are in order
        for n in col_names:
            col_values.append(data[n])

        self.database.insert_row("leaderboard", col_names, col_values)

        return self.new_response(200, "successful")

    def get_scores(self, mode_name):
        order_by = {"order_columns": ["score"], "sort_type": "DESC"}
        score_data = self.database.select_from_table("leaderboard", ["*"], ["level_mode"], [mode_name], order_by)
        data_names = self.database.get_table_column_names("leaderboard")
        # put each row of results into a dict with key of column name :)
        data = [dict(zip(data_names, s)) for s in score_data]

        return self.new_response(200, data)