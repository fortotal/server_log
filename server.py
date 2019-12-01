#!/usr/bin/env python3
import json
import socket

from flask import Flask
from flask import jsonify
from flask import request

import logging
import logging.config

import requests

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65430        # Port to listen on (non-privileged ports are > 1023)

hash = {}

appf = Flask(__name__)

logging.config.fileConfig('logging.conf')
logger = logging.getLogger("exampleApp")
logger.setLevel(logging.DEBUG)


@appf.route("/get", methods = ["GET"])
def get():
    resp = request.data.decode("utf-8")
    resp = json.loads(resp)
    logger.debug("get for key {}".format(resp["key"]))
    try:
        datafrHash = hash[resp["key"]]
        return json.dumps({"status": "Ok",
                          "message": datafrHash}).encode("utf-8")
    except KeyError:
        logger.warning("no data in cache for key [{}]".format(resp["key"]))
        return json.dumps({"status": "Not Found"}).encode("utf-8"), '404'
    except:
        return "Internal Server Error".encode("utf-8"), '403'


@appf.route("/delete", methods = ["DELETE"])
def delete():
    resp = request.data.decode("utf-8")
    resp = json.loads(resp)
    logger.debug("del for key [{}]".format(resp["key"]))
    try:
        del hash[resp["key"]]
        return json.dumps({"status": "OK"}).encode("utf-8")
    except KeyError:
        logger.warning("no data in cache for key [{}]".format(resp["key"]))
        return json.dumps({"status": "Not Found"}).encode("utf-8"), '404'
    except:
        return "Internal Server Error".encode("utf-8"), '403'


@appf.route("/put", methods = ["PUT"])
def put():
    resp = request.data.decode("utf-8")
    resp = json.loads(resp)
    logger.debug("put for key {}".format(resp["key"]))
    try:
        hash[resp["key"]] = resp["message"]
        return json.dumps({"status": "Create"}).encode("utf-8")
    except:
        logger.warning("Something bad")
        return "Internal Server Error".encode("utf-8"), '403'


if __name__ == '__main__':
    appf.run(host = HOST, port = PORT)
    
