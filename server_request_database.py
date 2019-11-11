
import server_request
import sql_query
import json
from Globals import Global

class ServerRequestDatabase(server_request.ServerRequest):

    def __init__(self, db_name, db_table_name, col_names, col_options):
        """
        :param db_name:             (str)  name of database
        :param db_table_name:       (str)  name of table in database
        :param col_names:           (List) name of columns in table
        """

        table_col_options = []
        cols = list( zip( col_names, col_options ) )

        for col in cols:
            table_col_options.append( ' '.join( col ) )

        table_cols_str = ', '.join( table_col_options )

        self.sql_db = sql_query.sql_query(db_name)
        self.sql_db.add_table(db_table_name, table_cols_str)

#                              self.table_col_names[0] + " INT, " +
#                              self.table_col_names[1] + " VARCHAR(255)"
#                              )

        self.table_name = db_table_name
        self.table_col_names = col_names  # ["spawn_time", "position"]

    def post_request(self, page_request, query, data):

        response = "Error: Not Found"
        status = 404

        if page_request.lower() == "/savedata":
            if query.lower() == "obj":
                response = self.add_data( data )
                status = 200

        return status, response

    def get_request(self, page_request, query):

        response = "Error: Not Found"
        status = 200

        if Global.DEBUG:
            print("Get Query:", query)

        if page_request.lower() == "/load":
            response = self.get_data(0)
        elif page_request.lower() == "/newGame".lower():
            response = self.get_data(0)
        elif page_request.lower() == "/delete" and query.split("=")[0] == "t":
            try:
                t = int(query.split("=")[1])
            except:
                t = 0
                print("Error: t was not an int :(")
            response = self.remove_data(t)
        elif page_request.lower() == "/clearTable".lower():
            response = self.clear_table()
        else:
            status = 404

        return status, response

    def get_data(self, time):
        """
        :param time: get all results after time. (0 if starting a new game)
        :return: string, of json, since 'time' or status if no data
        """

        if self.sql_db == None:         # create or get existing DB
            return "Error: No Database"

        # pull all data from the DB to be loaded into the game
        results = self.sql_db.select_from_table( self.table_name,
                                                 ', '.join(self.table_col_names),
                                                 "spwanTime > ?",
                                                 str(time) )
        row_data = []

        if results is None:
            return "Error: No Data"

        # stitch the col names and results together
        # appending it to row_data as a json str.
        for r in results:
            row = dict(zip(self.table_col_names, r))

            # check if the data starts with '{' if it does it need to be parshed into its own dict
            for key in row:
                # check that the row key does not start with { and ends in }
                if str(row[key])[0] == "{" and str(row[key])[-1] == "}":
                    row[key] = json.loads( row[key].replace("'", '"') )

            row_data.append( json.dumps( row ) )

            if Global.DEBUG:
                print("ADD: ", row_data[-1])

        if len(row_data) == 0:
            return "Error: No Data"
        else:
            return ';'.join( row_data )

    def add_data(self, json_data_str):
        """ Add data to table from json string

        :param json_data_str: json str of data to insert into table
        json keys must match table col names. (case-insensitive) (any others will be discarded)
        :return: status and message str( [status]:[message] )
        """
        if Global.DEBUG:
            print( "Add Data TO DB Json: ", json_data_str )  #.replace('\n', '').replace('\t', '').replace('\r', '') )

        json_data = json.loads( json_data_str )
        col_names = []
        data = []

        # find all data that matches table_col_names
        for j_col in json_data:
            for t_col in self.table_col_names:
                if j_col.lower() == t_col.lower():
                    col_names.append( j_col.lower() )
                    data.append( str(json_data[ t_col ] ) )
                    break

        if self.sql_db == None:
            return "Error: No Database"

        if len( col_names ) == 0:
            return "Error: No Data"
        if Global.DEBUG:
            print("col_names: ", col_names)

        self.sql_db.insert_row(self.table_name, col_names, data)

        return "Success: Row Added"

    def remove_data(self, time):
        """ Removes and object from the table.

        :param time: the time the object was spawned
        :return: status and message str( [status]:[message] )
        """

        if self.sql_db == None:
            return "Error: No Database"

        self.sql_db.remove_row(self.table_name, "spwanTime = ?", (str(time), ))

        return "Success: Row Removed"

    def clear_table(self):
        """ Causion: removes all values from table

                :return: status and message str( [status]:[message] )
        """

        if self.sql_db == None:
            return "Error: No Database"

        self.sql_db.remove_row(self.table_name, "spwanTime > ?", "0")

        return "Success: Row Removed"
