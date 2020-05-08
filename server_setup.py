from requestServers import server_request_amsql_explorer as amsql_explorer
from requestServers import server_request_pacman
from requestServers import server_trigger_webhook_event as server_webhook

class ServerSetup:

    def __init__(self, server):
        self.server = server

    def setup(self):
        # Start AMSql Explorer API
        AMSql = amsql_explorer.ServerRequest_AMSqlExplorer()
        AMSql.force_200_status = True
        self.add_callback("amsql", AMSql)

        # start Pacman API
        pacman = server_request_pacman.ServerRequest_Pacman()
        pacman.force_200_status = True
        self.add_callback("pacman", pacman)

        # TODO: remove above modules in the webhook master.
        # Webhook
        webhook = server_webhook.ServerWebhookTrigger()
        webhook.force_200_status = True
        self.add_callback("webhook", webhook)

    def add_callback(self, root_dir, _server_request):
        """ Adds the get and post function to the callbacks on server

        :param root_dir:        the root directory of the modules (/my_directory/)
        :param _server_request: instances of server request class
        :return:
        """
        self.server.post_callbacks[root_dir] = _server_request.post_request
        self.server.get_callbacks[root_dir] = _server_request.get_request
