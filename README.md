#Points
###Documentation for Backend Webservice

1. Background
2. Introduction
3. API
4. How to run
5. How to test
6. Requests
7. Future work

##Background / Problem Statement
Users have points in their account. They only see a single balance in their account. But for reporting purposes we actually track their points per payer/partner in our system. In our system each transaction record contains payer(string), points(integer) and timestamps(date).

For earning points it is easy to assign a payer, we know which actions earned the points. And thus which partner should be paying for the points.

When a user spends points, they don't know or care which payer the points come from. But, the accounting team does care how the points are spent.

There are two rules for determining what points to "spend" first:

● We want the oldest points to be spent first (oldest based on transaction timestamp, not the order they’re received)

● We want no payer's points to go negative.

##Introduction

This project uses `python` to perform server side operations and `flask` framework to build and host server which can cater to various types of API requests.

The project mainly consists of 2 parts: `server.py` and `points_record.py` along with a `ConfigFile.properties`.

`points_record.py`: We are using a double LinkedList to store and maintain data in ascending order as per timestamps. `class PointsRecord` is responsible to cater these requirements with the help of `add` and `spend` methods along with some helper functions.
This file is only for operations related to User Points. 

`server.py`: file contains the code to start the server, accepts and responds to various types of HTTP request, and initialize the InMemory data storage (for now -> LinkedList, this can be easily updated with database connection in future). This file is only for handling API requests.

`ConfigFile.properties`: This file contains the configuration for connection, API End Points, HTTP Status codes.

* The project design is flexible to accommodate adding new APIs, extending current work, or providing new features (The code maintains certain variables which can be used for this).

**In future when project expands, `server.py` can be separated into two different files, one for starting app, threading, db connection and another file for API request handling (or views).

##API
 
####1. [POST] /api/v1/add
The `ADD_POINTS` end point is used for adding user points. This API accepts only `POST` requests in form of json.
* url: `http://127.0.0.1:5000/api/v1/add`
* data(in json format): `{"payer": "DANNON", "points": 300, "timestamp": "2022-10-31T10:00:00Z"}`
* Expected response: A http request containing total points so far. `{'Total Points': 300}`
* Error handling: (1) If the request is not in json format (2) the data contains in request doesn't have proper keys. The keys should exactly match above-mentioned keys. (3) Any internal server error caused due to any other reasons.
* The web service returns appropriate HTTP status codes.

####2. [GET] /api/v1/balance
The `BALANCE_CHECK` end point is used for retrieving latest balance. This API accepts only `GET` requests.
* url: `http://127.0.0.1:5000/api/v1/balance`
* data(in json format): no input data expected
* Expected response: A http request containing total points so far. `{'DANNON': 1000, 'MILLER COORS': 5300, 'UNILEVER': 0}`
* Error handling: (1) Any internal server error caused due to any other reasons.
* The web service returns appropriate HTTP status codes.

####3. [POST] /api/v1/redeem
The `REDEEM_POINTS` end point is used for spending user points. This API accepts only `POST` requests in form of json.
* url: `http://127.0.0.1:5000/api/v1/redeem`
* data(in json format): `{"points": 5000 }`
* Expected response: A http request containing the points deducted from each payer. Deduction logic as per the timestamp in which they were credited. `[
{ "payer": "DANNON", "points": -100 },
{ "payer": "UNILEVER", "points": -200 },
{ "payer": "MILLER COORS", "points": -4,700 }
]`
* Error handling: (1) If the request is not in json format (2) If the user doesn't have sufficient points to redeem (3) the data contains in request doesn't have proper keys. The keys should exactly match above-mentioned key in request. (4) Any internal server error caused due to any other reasons.
* The web service returns appropriate HTTP status codes.

####4. [GET] /api/v1/reset
**This api is still in development.

The `RESET` end point is used for clearing user points data without the need of restarting the server. For now this API accepts only `GET`.
* url: `http://127.0.0.1:5000/api/v1/reset`
* data(in json format): No payload expected
* Expected response: A dummy response stating the data was reset in form of json.
* Error handling: in-development.


** In case of any issues with end points, Please refer to config file for latest end points.
##How To Run
###Pre-installed
* Python3.7 or higher

###Setup
1. Clone the code base in your local machine.
2. Navigate inside the code base directory.
3. Create a virtual environment

Windows
```
python -m venv env_name
```
or (if the PATH and PATHEXT are not configured)
```
C:\Users\{user_name}\AppData\Local\Programs\Python\{Python310}\python -m venv env_name
```
Linux
```
python3 -m venv env_name
```

4. Activate the environment

Windows
```
env_name\Scripts\activate
```
or
```
env_name\bin\activate
```

Linux
```
source env_name/bin/activate
```
Once the environment is activated user should see something like this in shell

Windows: (env_name) PS>

Linux: (env_name) $
5. Install the dependencies
6. ```
   pip install -r requirements.txt 
   ```
7. Check if all the requirements are installed successfully

###Start Server
By default the application will run on 127.0.0.1 and port 5000.
If user wants to change the default port, they can update the ConfigFile.properties file and update PORT variable.
```
[Windows] python server.py
[Linux] python3 server.py
```
This should start the server which is open to accept HTTP request and provide appropriate responses.


###How To Test
The code can be tested in following ways: 
1. Using Postman software for API querying
2. Using test.py script

Refer to file `how_to_test.pdf` for instructions.

###Requests
####Bad Request Scenarios
1. If an add request comes with zero points. [logic: it is expected, before calling the service, user should already validate points]
2. A payer e.g. "DANNON" has balance 500, and user wants to send add request with points -600, this request won't be accepted. (irrespective of total available points). An individual payer balance can not go in negative.
3. Total available points 1000 (DANNON: 500, MILLER COORS: 500), a redeem request of points > 1000 is received, it will be rejected (as total points can not go in negative). But if redeem request comes with 600 or 800 or points <= 1000, will be processed.


**Present code handles additional Bad request scenarios, which are not mentioned above. To be updated soon.
##Future Work
1. More loggers can be added to track the code performance.
2. Existing API end points can be enhanced to make them more robust, although the current end points handle good amount of ambiguity.
3. Add authentication in HTTP headers.