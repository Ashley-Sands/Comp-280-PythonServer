from requestServers import server_request
import sql_query as sql
import json
from helpers import Helpers as Help

class ServerRequest_Pacman( server_request.ServerRequest ):

    def __init__(self):

        # make sure that the database and required tables have been created
        self.database = sql.sql_query("pacman")

        # setup leader board table
        lb_table_cols = ["username", "ghost_killed", "pills_collected", "level",
                         "time", "score", "level_mode", "date_submitted"]

        lb_col_data_types = ["VARCHAR", "INT", "INT", "INT", "FLOAT", "INT", "VARCHAR", "INT"]

        self.database.add_table("leaderboard", lb_table_cols, lb_col_data_types)

        # setup game setting table
        gs_table_cols = ["setting_name", "number_value", "string_value"]
        gs_col_data_types = ["VARCHAR", "FLOAT", "VARCHAR"]

        self.database.add_table("game_settings", gs_table_cols, gs_col_data_types)
        self.add_default_settings()

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
        if page_request == "/settings" and "name" in query:
            response_data = self.get_settings(query["name"])

        return self.parse_response(response_data)

    def add_default_settings(self):
        """Adds default settings if they do not exist"""

        # define the default values (list of tuples [(key, value),...] )
        values = [("ghost_start_speed", 500),
                  ("ghost_speed_incress", 25),
                  ("start_ammo", 100),
                  ("start_lives", 10),
                  ("pill_respwan_time", 45),
                  ("powerPill_respwan_time", 60),
                  ("gun_clip_size", 10)]

        # check that the setting name does not exist
        for v in values:
            setting = self.database.select_from_table("game_settings", ["*"], ["setting_name"], [v[0]])
            if len(setting) < 1: # add the value if no setting was returned.
                self.database.insert_row("game_settings", ["setting_name", "number_value"], [v[0], v[1]])

        print("Default GameSetting: OK!")

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
        data = self.zip_column_names("leaderboard", score_data)

        return self.new_response(200, data)

    def get_settings(self, setting_name):

        where_cols = []
        where_data = []

        if setting_name != "ALL":
            where_cols.append("setting_name")
            where_data.append(setting_name)

        setting_data = self.database.select_from_table("game_settings", ["*"], where_cols, where_data)

        data = self.zip_column_names("game_settings", setting_data)

        return self.new_response(200, data)

    def zip_column_names(self, table_name, table_data):
        """Zips data from into a dict where the keys are column names"""
        data_names = self.database.get_table_column_names(table_name)
        # put each row of results into a dict with key of column name :)
        if data_names is not None and table_data is not None:
            return [dict(zip(data_names, s)) for s in table_data]
        else:
            return []
