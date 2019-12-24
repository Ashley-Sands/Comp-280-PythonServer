from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from requestServers import server_request_database, server_request_amsql_explorer as amsql_explorer, server_request

from Globals import GlobalConfig

# config
GlobalConfig.set("host", "127.0.0.1")
GlobalConfig.set("port", 8000)
GlobalConfig.set("db_root", "databases/")

host = "127.0.0.1"
port = 8000

class Server(BaseHTTPRequestHandler):
    # Both use the first part of path as key (ie if url = 'abc.com/path_p0/path_p1/page.html' key = 'path_p0' )
    post_callbacks = {}   # callback sig: (request, data   )
    get_callbacks  = {}   # callback sig: (request         )

    def do_POST(self):
        print( "POST request: ", self.path )

        # get the content from the post request
        content_len = int( self.headers['Content-Length'] )
        post_data = self.rfile.read(content_len)

        if Global.DEBUG:
            print("Data: ", post_data)

        # process request
        self.request = urlparse(self.path)
        status, response_data = self.process_callbacks(self.post_callbacks, post_data)

        # send headed
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.send_header('Access-Control-Allow-origin', '*')
        self.end_headers()
        # reply
        self.wfile.write(response_data.encode())

    def do_GET(self):
        print("GET request: " + self.path)

        # process request
        self.request = urlparse(self.path)
        status, response_data = self.process_callbacks(self.get_callbacks)

        # send headed
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.send_header('Access-Control-Allow-origin', '*')
        self.end_headers()
        # reply
        self.wfile.write(response_data.encode())

    def process_callbacks(self, callbacks, post_data=None):

        status = 404
        response_data = ()
        response = ""
        dir_root = self.request.path.split("/")[1]
        path = '/'.join( self.request.path.split("/")[2:] )
        path = "/" + path

        print(dir_root, path)

        # remove all trailing '/' if any
        while len(path) > 0 and path[-1] == "/":
            path = path[:-1]

        if dir_root in callbacks:
            print("HaveKEY")
            if post_data is None:
                response_data = callbacks[dir_root]( path, self.request.query )
            else:
                response_data = callbacks[dir_root]( path, self.request.query, post_data.decode('utf-8') )

            status = response_data[0]

            if status == 200:
                response = response_data[1]

        return status, response


print("- Run Test.py to test sql_query ")
print("- Starting...")
# set up the request callbacks.
request = server_request.ServerRequest();

Server.post_callbacks["test"] = request.post_request
Server.get_callbacks["test"]  = request.get_request

# Create the game data callbacks
game_data_request = server_request_database.ServerRequestDatabase("cube_killer", "game_data",
                                                                  ["spwanTime", "position",     "scale"],
                                                                  ["INT",       "VARCHAR(255)", "VARCHAR(255)"]
                                                                  )

Server.post_callbacks["game"] = game_data_request.post_request
Server.get_callbacks["game"]  = game_data_request.get_request

# Start AMSql Explorer API
AMSql = amsql_explorer.ServerRequest_AMSqlExplorer()
Server.post_callbacks["amsql"] = AMSql.post_request
Server.get_callbacks["amsql"]  = AMSql.get_request

server = HTTPServer( (GlobalConfig.get("host"), GlobalConfig.get("port")), Server )

print("- Waiting on you request...")

while True:
    server.serve_forever()

server.server_close()
