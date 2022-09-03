# stackpath-aggr-system-task
An aggreagation system that receives counters and aggregates them to be able to show statistics about those counters


1. The service accepts JSON objects (counters) over HTTP. An example of a counter is:
    ```json
    { "timestamp": 1608102631, "siteA.com": 3, "siteB.com": 4 }
    ```
    The object will always contain the timestamp key with the value in Unix epoch time and optionally multiple other keys for each domain in the counter, with the value being the number of requests.

2. The service can retrieve the following statistics:

    - The ten domains with the most traffic in the last full minute, ordered by count.

    - The ten domains with the most traffic in the last full hour, ordered by count.

    The statistics are returned as JSON objects as well.

 
### Assumptions:

1. Counter objects can come from different sources, so the service should support receiving multiple counters for the same timestamps and domains.

2. A full minute is the last complete minute; for example, if the current time is 10:22:05 data should be returned for 10:21:00-10:22:00.

3. A full hour is the last complete hour; for example, if the current time is 10:22:05 data should be returned for 9:00:00-10:00:00.

4. All times are in UTC.


# Usage

## Start the server locally
```bash
$ python3 src/server.py
```
The server will run on port `3000` by default.

# API    
## Add counters
`POST /api/counters`
```bash
$ curl -X POST 'http://localhost:3000/api/counters -d { "timestamp": "1661860794425l", "siteA.com": 3, "siteB.com": 4, "siteC.com": 7 }
```
   
## Receive statistics of top ten domains in the last minute
The ten domains with the most traffic in the last full minute, ordered by count.

`GET /api/stats/lastMinute`
```bash
$ curl 'http://localhost:3000/api/stats/lastMinute'

[{ "domain": "siteC.com", "count": 7 }, { "domain": "siteB.com", "count": 4 }, { "domain": "siteA.com", "count": 3 }]
```            


## Receive statistics of top ten domains in the last hour
The ten domains with the most traffic in the last full hour, ordered by count.

`GET /api/stats/lastHour`
```bash
$ curl 'http://localhost:3000/api/stats/lastHour'

[{ "domain": "siteC.com", "count": 1377 }, { "domain": "siteA.com", "count": 435 }, { "domain": "siteB.com", "count" :312 }]
```            
    
 # Tests

 ## Run unit tests
```bash
test/$ python3 system/test_stats.py
```
 ## Run integration tests 
 (this is not fully covered at the moment as I had some issues and I didn't want to spend too long on fixing them, but the idea is well written there)
```bash
test/$ python3 integration/api/test_routes.py
```

# Notes
This is quite a basic version of the assignment. It includes the logic and some tests, but there are a few things missing obviously:
1. The integration tests are almost fully written, but issues I encountered together with not wanting to delay this assignment submission time didn't allow me to make it pass. I did perform a manual QA for this type of check, and it all looked as it is working seamlessly.
2. Still need to add a Dockerfile to support that as well.
3. Due to time constraints, the DB is currently a simple JSON file, but should rather be a MongoDB instance (more about this choice is explained in the code).
4. If I had more time I would have created an interface/schema for the objects being saved in the DB.
5. Much more error handling is needed here of course.
6. I couldn't find how to make tests runnable from the root folder, hence the need to run them from the `test/` folder.
7. The node environment, the server's port and the future MongoDB url should all be configurable.
8. A proper logger is also missing.
