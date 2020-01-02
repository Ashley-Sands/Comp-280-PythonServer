from requestServers import server_request_amsql_explorer as amsql_explorer
from requestServers import server_request_pacman

class ServerSetup:

    def __init__(self, server):
        self.server = server

    def setup(self):
        # Start AMSql Explorer API
        AMSql = amsql_explorer.ServerRequest_AMSqlExplorer()
        AMSql.force_200_status = True
        self.server.post_callbacks["amsql"] = AMSql.post_request
        self.server.get_callbacks["amsql"] = AMSql.get_request

        # start Pacman API
        pacman = server_request_pacman.ServerRequest_Pacman()
        pacman.force_200_status = True
        self.server.post_callbacks["pacman"] = pacman.post_request
        self.server.get_callbacks["pacman"] = pacman.get_request
