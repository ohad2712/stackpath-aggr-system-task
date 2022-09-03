from http.server import  BaseHTTPRequestHandler, HTTPServer
import ssl
from enum import Enum
from collections import defaultdict
import json
import time
import os,sys
sys.path.insert(0, os.path.abspath("."))

from src.statistics import StatisticsHandler


global data
data = defaultdict(lambda: {})

class RoutePaths(Enum):
    LAST_MINUTE_STATS = '/api/stats/lastMinute'
    LAST_HOUR_STATS = '/api/stats/lastHour'
    COUNTERS = '/api/counters'

class EndpointsHandler(BaseHTTPRequestHandler):
    # Sets basic headers for the server
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/json')
       
        length = int(self.headers['Content-Length'])
        
        # Reads the contents of the request
        content = self.rfile.read(length)
        headers = str(content).strip('b\'')
       
        self.end_headers()
        
        return headers

    def do_GET(self):
        stats = StatisticsHandler()
        
        now = time.time()
        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.end_headers()

        if self.path == RoutePaths.LAST_MINUTE_STATS.value:
            last_minute_stats = stats.get_last_minute_domains(now) # This will fetch everything from the MongoDB using the query from the js example

            self.wfile.write(json.dumps(minutes).encode())
        elif self.path == RoutePaths.LAST_HOUR_STATS.value:
            last_hour_stats = stats.get_last_hour_domains(now)

            self.wfile.write(json.dumps(last_hour_stats).encode())
        else:
            pass
       
          
    def do_POST(self):
        headers = self._set_headers()
        stats = StatisticsHandler()
        if self.path == RoutePaths.COUNTERS.value:
            data = json.loads(headers)
            stats.write_stats(data) # This writes the changes to the json file (and in the future to the MongoDB instance)
        else:
            pass
    

server = HTTPServer(('', 3000), EndpointsHandler)

# If certs are needed, add this code:
# server.socket = ssl.wrap_socket (server.socket, 
#         keyfile="path/to/key.pem", 
#         certfile='path/to/cert.pem', server_side=True)

def start_server():
    server.serve_forever()

def close_server():
    server.shutdown()

start_server()
