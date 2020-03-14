# Python HTTP Server

### Running the server
Run '/main/build.exe' to run the standalone build of the http server  
The server has been build using PyInstaller 3.5  
To run the web server from source run ```main_server.py``` using python 3.7  
With mysql-connector installed (use master branch if you only need sqlite support)

### Extending the server

#### Creating a server module
Override ```server_request.ServerRequest```  
Add POST logic to ```post_request``` function and GET logic to ```get_request``` function  
both GET and POST function MUST return a tuple with ```response status, page content```  
Use ```parse_response``` function to parse the page content into a json string.  
The Json string contains the ```response status``` and the ```page content```  
it is possible to force the response status to ```200 (OK)``` while the Json string  
contains the true status by setting ```force_200_status = True```. This is helpful  
for APIs allowing you to send improved error messages.  
Use ```new_response``` function to format the json string as ```{"status": status, "response": {response_data}}```

(For more info see doc strings)

#### Adding the module to the server
Locate file 'server_setup.py' and create an instances of your server_request class
in the ```setup``` function and call ```self.add_callback``` with params root_dir 
and the server_request instances.  
**DONE!**

#### Other 
see ```sql_query.py``` for MYSQL/SQLite helper functions; or  
checkout to the 'master' branch if only requiring SQLite support  
(MYSQL Support has **NOT** been tested with ```AMSqlite Explorer```)
see ```helpers.py``` for general helper functions  
host, port and database_root can be changed at the top of main server  
```
# config
GlobalConfig.set("host", "127.0.0.1")
GlobalConfig.set("port", 8000)
GlobalConfig.set("db_root", "databases/")
```

### Running the UnitTest 
Run ```Test.py``` using python 3.7
