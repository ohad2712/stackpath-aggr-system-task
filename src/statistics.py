import datetime
import json
from collections import Counter, defaultdict
from itertools import takewhile
import os, sys
sys.path.insert(0, os.path.abspath(".."))

TOP = 10

class StatisticsHandler:
    data = defaultdict(lambda: {})

    get_hour = lambda self, epoch_time: int(str(datetime.datetime.fromtimestamp(float(epoch_time)))[11:].split(":")[0])
    '''Returns the current hour according to the current epoch'''

    get_minute = lambda self, epoch_time: int(str(datetime.datetime.fromtimestamp(float(epoch_time)))[11:].split(":")[1]) 
    '''Returns the current minute according to the current epoch'''

    get_date = lambda self, epoch_time: str(datetime.datetime.fromtimestamp(float(epoch_time)))[:10]
    '''Returns the current date according to the current epoch'''
    
    def get_last_hour_domains(self, epoch_time):
        domains = self.domains_list()

        last_hour_domains = []
        last_hour_epoch = int(epoch_time) - (60 * 60)
        last_hour = self.get_hour(str(last_hour_epoch))
        last_hour_day = self.get_date(str(last_hour_epoch)[8:]) # The last-hour's day value

        for domain in domains:
            timestamp = domain["timestamp"]
            domain_timestamp_day = self.get_date(str(timestamp)[8:])
            if (
                self.get_hour(timestamp) == last_hour
                and last_hour_day == domain_timestamp_day
            ):
                last_hour_domains.append(domain)
        
        return last_hour_domains

    def get_last_minute_domains(self, epoch_time):
        domains = self.domains_list()

        last_minute_domains = []
        last_minute_epoch = int(epoch_time) - 60
        last_minute = self.get_minute(str(last_minute_epoch))
        hour_last_minute = self.get_hour(str(last_minute_epoch))
        last_minute_day = self.get_date(str(last_minute_epoch)[8:]) # The last-minute's day value

        for domain in domains:
            timestamp = domain["timestamp"]
            domain_timestamp_day = self.get_date(str(timestamp)[8:])
            domain_timestamp_minute = self.get_minute(timestamp)
            domain_timestamp_hour = self.get_hour(timestamp)
            if (
                domain_timestamp_minute == last_minute
                and domain_timestamp_day == last_minute_day
                and domain_timestamp_hour == hour_last_minute
            ):
                last_minute_domains.append(domain)

        return last_minute_domains

    def get_last_round_hour_domains(self, epoch_time):
        # If that was supported by a MongoDB instance 
        # this would include a find with a query looking like { timestamp: { $gt: epoch_time } } with sorting it properly as well
        ''' Calculates the last round hour according to the current epoch, and returns a list of domains according to that. '''

        domains_last_hour = []

        for domain in self.get_last_hour_domains(epoch_time):
            # Create list of domains in the last round hour in a dictionary {"domain": numberOfRequests}
            for key, value in domain.items():
                if key != "timestamp":
                    domains_last_hour.append({ key: value })
        
        return domains_last_hour

    def get_last_round_minute_domains(self, epoch_time):
        # If that was supported by a MongoDB instance 
        # this would include a find with a query looking like { timestamp: { $gt: epoch_time } } with sorting it properly as well
        ''' Calculates the last round minute according to the current epoch, and returns a list of domains according to that. '''
        domains_last_minute = []

        for domain in self.get_last_minute_domains(epoch_time):
            # Create list of domains in the last round minute in a dictionary {"domain": numberOfRequests} 
            for key, value in domain.items:
                if key != "timestamp":
                    domains_last_minute.append({ key: value })

        return domains_last_minute

    def domains_list(self):
        # In case it is really supported by a MongoDB instance this function would perform a simple saving to the DB with the proper object,
        # instead of dealing with fs manipulations
        ''' Returns a list of all domains from db '''
        req_list = []

        script_dir = os.path.dirname(__file__)
        rel_path = "db/db.json"
        abs_file_path = os.path.join(script_dir, rel_path)
       
        # Read from db.json
        with open(abs_file_path, 'r') as f:
            res = f.read()
            final = json.loads(res)
            for key in final.keys():
                req_list.append(final[key])
        
        return req_list

    def get_items_upto_count(self, counter, n):
        ''' Returns top n common items in a counter 
        (with same value items counted as a single result,
        i.e. the top 2 for [{ 'A': 2 }, { 'B': 1 }, { 'C': 1 }] will be the whole dictionary [as 'B' and 'C' both has `1` as the value])
        '''
        data = counter.most_common()
        last_matching_item_value = data[n-1][1] # Get the value of (n-1) item
        
        # Now collect all items whose value is greater than or equal to `val`.
        return list(takewhile(lambda x: x[1] >= last_matching_item_value, data))
    
    def get_most_common_domains(self, epoch_time, top = TOP):
        ''' Returns the top `top` (10) most common domains in the last round minute according to their epoch as a dictionary. '''
        
        # Getting all last round minute domains
        last_minute_domains = self.get_last_round_minute_domains(epoch_time)
        top_domains = defaultdict(lambda:0)
        
        for dom in last_minute_domains:
            for key, value in dom.items():
                top_domains[key] += value
        
        # If there are less than `top` (10) domains, we should return all the domains there are
        if len(top_domains) < top:
            top = len(top_domains)
       
        top_domain_counters = [{ domain_counter[0] :domain_counter[1] } for domain_counter in self.get_items_upto_count(Counter(top_domains),top)]

        # The returned array will look like [{ 'siteA': 5 }, ...]
        return top_domain_counters


    def get_top_x_last_hour_domains(self, epoch_time, top = TOP):
        ''' Returns the top `top` (10) most common domains in the last round hour according to their epoch as a dictionary. '''
        
        #Getting all last round hour domains
        last_hour_domains = self.get_last_round_hour_domains(epoch_time)
        top_domains = defaultdict(lambda: 0)
        
        for dom in last_hour_domains:
            for key, value in dom.items():
                top_domains[key] += value
       
        #If there are less than `top` (10) domains, we should return all the domains there are
        if len(top_domains) < top:
            top = len(top_domains)

        top_domain_counters = [{ domain_counter[0]: domain_counter[1] } for domain_counter in self.get_items_upto_count(Counter(top_domains),top)] 
        
        # The returned array will look like [{ 'siteA': 5 }, ...]
        return top_domain_counters

    key = 0
    db_file_rel_path = 'db/db.json'
    
    def write_stats(self, req_data):
        # This should be using a MongoDB instance, as all objects might differ in structure.
        # This way we can easily insert any object representing the relevant counters coming in to this service,
        # while being able to support a big amount of documents in the system.
        # Moreover, no joins or specific relations between tables is required, so a SQL DB is not needed for this system's purpose.
        ''' Writes stats to the db.json file '''
        for self.key, value in StatisticsHandler.data.items():
            pass

        index = int(self.key) + 1
        StatisticsHandler.data[index] = req_data
        script_dir = os.path.dirname(__file__)
        abs_file_path = os.path.join(script_dir, db_file_rel_path)
        
        with open(abs_file_path, 'w+') as file_data:
            json.dump(StatisticsHandler.data, file_data)
        
        return True

    
    def reset_db(self):
        # This should be for closing the MongoDB instance while clearing it out beforehand 
        ''' Delete the db.json file content '''
        script_dir = os.path.dirname(__file__)
        abs_file_path = os.path.join(script_dir, db_file_rel_path)
        self.key = 0
        
        with open(abs_file_path, 'w+') as file_data:
            StatisticsHandler.data.clear()
            json.dump(StatisticsHandler.data, file_data)
        
        return True
        
