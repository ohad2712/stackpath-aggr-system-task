import datetime
import json
import requests
import sys, os
sys.path.insert(0, os.path.abspath(".."))

from src.server import start_server, close_server

PORT = 3000

class Test_APIRoutes(unittest.TestCase):
    local_server_url_prefix = f"http://localhost:{PORT}"

    def add_counters(self, payload):
        ''' This function sends a POST request to /api/counters to add counters '''
        response = requests.post(
            f'{local_server_url_prefix}/api/counters',
            json.dumps(payload),
        )

        if response.status_code != 200:
            return { ok: False }
        
        return { ok: True }
   
    def setUp(self):
        start_server()
        pass
        
    def tearDown(self):
        close_server()
        # Add resetting and then connection closing for the DB
        pass

    def test_add_counters(self):
        now = datetime.now
        currentYear = now.year
        currentMonth = now.month
        currentDay = now.day

        for i in range(10):
            response = self.add_counters(
                { 
                    "timestamp": str(datetime.datetime(2022, 1, 15, i, i+3, 0).timestamp()).split('.')[0],
                    "siteA.com": 3,
                    "siteB.com": 90,
                }
            )

            self.assertEqual(response, { ok: True })
    
    def test_receive_last_minute_stats(self):
        response = requests.get(f'{local_server_url_prefix}/api/stats/lastMinute')
        self.assertEqual(response.status_code, 200)
        # To do- Add assertion according to the returned response here
        self.assertEqual(response.data, {})
        print(response)


    def test_receive_last_hour_stats(self):
        response = requests.get(f'{local_server_url_prefix}/api/stats/lastHour')
        self.assertEqual(response.status_code, 200)
        # To do- Add assertion according to the returned response here
        self.assertEqual(response.data, {})
        print(response)