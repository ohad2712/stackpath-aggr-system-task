import unittest
from unittest.mock import patch
import datetime
import time
import json

import os, sys
sys.path.insert(0, os.path.abspath(".."))

from src.statistics import StatisticsHandler as sts

class Test_Satatistics(unittest.TestCase):
   
    def setUp(self):
        self.counter1_date = str(datetime.datetime(2022, 9, 2, 0, 1, 0).timestamp()).split('.')[0]
        self.counter2_date = str(datetime.datetime(2022, 9, 1, 23, 58, 0).timestamp()).split('.')[0]
        self.counter3_date = str(datetime.datetime(2022, 9, 2, 0, 0, 0).timestamp()).split('.')[0]
        self.counter4_date = str(datetime.datetime(2022, 9, 1, 23, 59, 0).timestamp()).split('.')[0]
        
        self.stats = sts()
        
    def tearDown(self):
        # This should reset and then lose the connection with the DB instance

        # self.stat = sts()
        # self.stat.reset_db()
        pass

    # Test POST to DB
    def test_write_stats(self):
        counter_data1 = { 'timestamp': self.counter3_date, 'siteA.com': 3, 'siteB.com': 45 }
        counter_data2 = { 'timestamp': self.counter2_date, 'siteH.com': 13, 'siteK.com': 15, 'siteC.com': 3, 'siteG.com': 20 }
        counter_data3 = { 'timestamp': self.counter4_date, 'siteA.com': 1, 'siteB.com': 45, 'siteO.com': 67, 'siteD.com': 95 }
        counter_data4 = { 'timestamp': self.counter1_date, 'siteD.com': 87, 'siteV.com': 14, 'siteI.com': 56, 'siteR.com': 2 }
        
        self.assertEqual(self.stats.write_stats(counter_data1), True)
        self.assertEqual(self.stats.write_stats(counter_data2), True)
        self.assertEqual(self.stats.write_stats(counter_data3), True)
        self.assertEqual(self.stats.write_stats(counter_data4), True)


    # Test getting the hour for a date
    def test_get_hour(self):
        self.assertEqual(self.stats.get_hour(self.counter1_date),0)
        self.assertEqual(self.stats.get_hour(self.counter2_date), 23)
        self.assertEqual(self.stats.get_hour(self.counter3_date), 0)
        self.assertEqual(self.stats.get_hour(self.counter4_date), 23)


    # Test getting the minute for a date
    def test_get_minute(self):
        self.assertEqual(self.stats.get_minute(self.counter1_date), 1)
        self.assertEqual(self.stats.get_minute(self.counter2_date), 58)
        self.assertEqual(self.stats.get_minute(self.counter3_date), 0)
        self.assertEqual(self.stats.get_minute(self.counter4_date), 59)


    # Test getting the date for a date
    def test_get_date(self):
        self.assertEqual(self.stats.get_date(self.counter1_date), '2022-09-02')
        self.assertEqual(self.stats.get_date(self.counter2_date), '2022-09-01')
        self.assertEqual(self.stats.get_date(self.counter3_date), '2022-09-02')
        self.assertEqual(self.stats.get_date(self.counter4_date), '2022-09-01')

    def test_domains_list(self):        
        expected_domains_list = [
            { 'timestamp': '1662065940', 'siteA.com': 1, 'siteD.com': 95, 'siteO.com': 67, 'siteB.com': 45 },
            { 'timestamp': '1662066000', 'siteA.com': 3, 'siteB.com': 45 },
            { 'timestamp': '1662066060', 'siteD.com': 87, 'siteI.com': 56, 'siteR.com': 2, 'siteV.com': 14 },
            { 'timestamp': '1662065880', 'siteH.com': 13, 'siteC.com': 3, 'siteG.com': 20, 'siteK.com': 15 }
        ]

        self.assertCountEqual(self.stats.domains_list(), expected_domains_list)
            
    def test_get_top_x_last_hour_domains(self):
        expected_domains_list = [
            { 'siteD.com': 95 },
            { 'siteO.com': 67 },
            { 'siteB.com': 45 },
            { 'siteG.com': 20 },
            { 'siteK.com': 15 },
            { 'siteH.com': 13 },
            { 'siteC.com': 3 },
            { 'siteA.com': 1 },
        ]
        
        self.assertEqual(self.stats.get_top_x_last_hour_domains(self.counter3_date), expected_domains_list);
   
    def test_get_most_common_domains(self):
        expected_domains_list = [
            { 'siteG.com': 20 },
            { 'siteK.com': 15 }, 
            { 'siteH.com': 13 }, 
            { 'siteC.com': 3 },
        ]
        
        self.assertEqual(self.stats.get_most_common_domains(self.counter4_date), expected_domains_list)

    #def test_reset_db(self):
        #self.assertEqual(self.stats.reset_db(), True)

if __name__ == "__main__":
    unittest.main()
