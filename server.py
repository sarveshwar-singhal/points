import sys
from flask import Flask, Response, request, json, jsonify
import configparser
import logging
import time

from points_record import PointsRecord


#GLOBAL Variables
app = Flask(__name__)
config = configparser.RawConfigParser()
config.read("ConfigFile.properties")
HOST = config.get('Connection','HOST')
PORT = config.get('Connection','PORT')
API_END_POINTS = 'APIEndPoints'
HTTP_STATUS_CODES = 'HTTPStatusCodes'
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.ERROR)

# User requests Data persisted during server run
DATA_LL = PointsRecord()
DUMMY_MSG = {'dummy':'dummy response'}
MIMETYPE ='application/json'


@app.post(config.get(API_END_POINTS,'ADD_POINTS'))
def add_points():
    """
    This method is used to accept the post request on add_points api. It will take data from request body and send it to Add method in PointsRecord() class.
    :return: flask.Response | and returns just the total point.
    """
    logging.info(f"{config.get(API_END_POINTS,'ADD_POINTS')} call started")
    # time.sleep(1)  #to validate the timestamps of requests
    output = DUMMY_MSG.copy()
    status = config.get(HTTP_STATUS_CODES, 'CONTINUE')
    try:
        if request.is_json:
            transaction = request.json
            is_valid = DATA_LL.add(**transaction)
            output.clear()
            if is_valid:
                output["Total Points"] = DATA_LL.total_points
                status = config.get(HTTP_STATUS_CODES, 'CREATED')
            else:
                output['error'] = "Invalid entry. Possible cause: 1. Either this payer is coming first time with negative points. or 2. This payer already exists in system but the points requested to be added will result in negative balance for that payer. or 3. User wants zero points to be added against a payer."
                status = config.get(HTTP_STATUS_CODES, 'BAD_REQUEST')
        else:
            status = config.get(HTTP_STATUS_CODES, 'BAD_REQUEST')
            output.clear()
            output['error'] = "The request should be in JSON format"
    except TypeError as te:
        logging.exception("Exception Occurred", exc_info=True)
        status = config.get(HTTP_STATUS_CODES, 'BAD_REQUEST')
        output.clear()
        output['error'] = "Key mismatch"
    except Exception as err:
        logging.exception("Exception Occurred", exc_info=True)
        output.clear()
        output['error'] = "Internal server error occurred while processing your request"
        status = config.get(HTTP_STATUS_CODES, 'INTERNAL_SERVER_ERROR')
    logging.info(f"{config.get(API_END_POINTS, 'ADD_POINTS')} call ended")
    return Response(json.dumps(output), status=status, mimetype=MIMETYPE)


@app.get(config.get(API_END_POINTS,'BALANCE_CHECK'))
def get_balance():
    """
    This method returns the total points corresponding to each payer in form of dictionary.
    :return: flask.Response
    """
    logging.info(f"{config.get(API_END_POINTS, 'BALANCE_CHECK')} call started")
    output = DUMMY_MSG.copy()
    status = config.get(HTTP_STATUS_CODES, 'CONTINUE')
    try:
        output = DATA_LL.entire_info
        logging.info(output)
        status = config.get(HTTP_STATUS_CODES, 'OK')
    except Exception as err:
        logging.exception("Exception Occurred", exc_info=True)
        status = config.get(HTTP_STATUS_CODES, 'INTERNAL_SERVER_ERROR')
        output.clear()
        output['error'] = "Internal server error occurred while processing your request"
    logging.info(f"{config.get(API_END_POINTS, 'BALANCE_CHECK')} call ended")
    return Response(json.dumps(output, sort_keys=False), status=status, mimetype=MIMETYPE)


@app.post(config.get(API_END_POINTS, 'REDEEM_POINTS'))
def redeem_points():
    """
    Reads users requests, if user doesn't have sufficient points it informs the user, otherwise deduct the points from the oldest timestamp to the latest timestamp record.
    :return: flask.Response | contains payer info along with deducted amount.
    """
    logging.info(f"{config.get(API_END_POINTS, 'REDEEM_POINTS')} call started")
    outcome = DUMMY_MSG.copy()
    status = config.get(HTTP_STATUS_CODES, 'CONTINUE')
    try:
        if request.is_json:
            requirement = request.json
            status = config.get(HTTP_STATUS_CODES, 'OK')
            if requirement['points'] > DATA_LL.total_points:
                outcome.clear()
                outcome['error'] = 'insufficient balance'
            else:
                deduct_info = DATA_LL.spend(requirement['points'])
                #formatting the output as per the API call requirement
                deduct_info_format = [{"payer":key, "points":value} for key, value in deduct_info.items()]
                outcome = deduct_info_format
        else:
            outcome.clear()
            outcome['error'] = "The request should be in JSON format"
            status = config.get(HTTP_STATUS_CODES, 'BAD_REQUEST')
    except KeyError as ke:
        logging.exception("Exception Occurred", exc_info=True)
        outcome.clear()
        outcome['error'] = "Key not found. Expected key 'points'"
        status = config.get(HTTP_STATUS_CODES, 'BAD_REQUEST')
    except Exception as err:
        logging.exception("Exception Occurred", exc_info=True)
        status = config.get(HTTP_STATUS_CODES, 'INTERNAL_SERVER_ERROR')
        outcome.clear()
        outcome['error'] = "Internal server error occurred while processing your request"
    logging.info(f"{config.get(API_END_POINTS, 'REDEEM_POINTS')} call ended")
    return Response(json.dumps(outcome), status=status, mimetype=MIMETYPE)


@app.get(config.get(API_END_POINTS, 'PRINT_ALL_DATA'))
def print_all_data():
    """
    this is server side method to print the existing LinkedList. This method was created for testing purpose.
    For now the access to this method has been revoked.
    :return:
    """
    output = dict()
    logging.info(f"in function: {sys._getframe().f_code.co_name}")
    DATA_LL.print()
    output['info'] = "Data printed"
    return jsonify(output)


# @app.get('/reset')
@app.get(config.get(API_END_POINTS, 'RESET'))
def resetLL():
    """
    This method was created to reset the LinkedList. In case the user doesn't want to restart the server but reset the existing data, then this end point can be used to clear the user data.
    :return: DUMMY_MSG
    """
    DATA_LL.clear()
    DUMMY_MSG.clear()
    DUMMY_MSG['info'] = "Data Cleared"
    return jsonify(DUMMY_MSG)


@app.route('/')
def index():
    return jsonify({'msg':"Server Started"})


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
    # app.run(debug=True)
