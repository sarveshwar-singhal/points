import requests
import time
import datetime
import configparser

config = configparser.RawConfigParser()
config.read('ConfigFile.properties')
API_END_POINTS = 'APIEndPoints'
HOST = config.get('Connection', 'HOST')
PORT = config.get('Connection', 'PORT')

def add_data(url):
    api = config.get(API_END_POINTS,'ADD_POINTS')
    url += api
    data = [{ "payer": "DANNON", "points": 300, "timestamp": "2022-10-31T10:00:00Z" }
        ,{ "payer": "UNILEVER", "points": 200, "timestamp": "2022-10-31T11:00:00Z" }
        ,{ "payer": "DANNON", "points": -200, "timestamp": "2022-10-31T15:00:00Z" }
        ,{ "payer": "MILLER COORS", "points": 10000, "timestamp": "2022-11-01T14:00:00Z" }
        ,{ "payer": "DANNON", "points": 1000, "timestamp": "2022-11-02T14:00:00Z" }]
    data = [{"payer": "DDANNON", "points": 0, "timestamp": "2022-10-31T10:00:00Z"}]
    # data = [{"payer": "DANNON", "points": 300, "timestamp": "2022-10-31T10:00:00Z"}
    #     , {"payer": "UNILEVER", "points": 200, "timestamp": "2022-10-31T11:00:00Z"}
    #     , {"payer": "DANNON", "points": -200, "timestamp": "2022-10-31T15:00:00Z"}
    #     , {"payer": "MILLER COORS", "points": 10000, "timestamp": "2022-09-01T14:00:00Z"}
    #     , {"payer": "DANNON", "points": 1000, "timestamp": "2022-10-31T14:00:00Z"}]
    # data = [{"payer": "DANNON", "points": 299, "timestamp": "2022-10-31T10:00:00Z"}
    #     , {"payer": "UNILEVER", "points": 199, "timestamp": "2022-10-31T11:00:00Z"}
    #     , {"payer": "DANNON", "points": -199, "timestamp": "2022-10-31T15:00:00Z"}
    #     , {"payer": "MILLER COORS", "points": 10000, "timestamp": "2022-11-01T14:00:00Z"}
    #     , {"payer": "DANNON", "points": 1000, "timestamp": "2022-11-02T14:00:00Z"}]
    t1 = time.time()
    for rec in data:
        resp = requests.post(url=url, json=rec)
        print_resp(resp)
    t2 = time.time()
    print(t2-t1)
    return

def print_all_data(url):
    api = config.get(API_END_POINTS, 'PRINT_ALL_DATA')
    url += api
    resp = requests.get(url)
    print_resp(resp)
    return

def get_balance(url):
    api = config.get(API_END_POINTS, 'BALANCE_CHECK')
    url += api
    resp = requests.get(url)
    print_resp(resp)
    return

def redeem_points(url):
    api = config.get(API_END_POINTS, 'REDEEM_POINTS')
    url += api
    data = {"points":6300}
    resp = requests.post(url, json=data)
    print_resp(resp)
    return


def print_resp(resp:requests.Response):
    print(f"status code {resp.status_code}, with message: {resp.json()}")
    return


def reset(url):
    # api = "/reset"
    api = config.get(API_END_POINTS, 'RESET')
    url += api
    resp = requests.get(url)
    return

def main():
    domain = "http://" + HOST
    port = PORT
    url = domain + ":" + port
    # reset(url)
    # add_data(url)
    get_balance(url)
    print_all_data(url)
    # redeem_points(url)
    return


if __name__ == "__main__":
    main()