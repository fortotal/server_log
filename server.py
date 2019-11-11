#!/usr/bin/env python3
import json
import socket

from flask import Flask
from flask import jsonify
from flask import request

import logging

import unittest
import requests

#class TestStringMethods(unittest.TestCase):
#
#    def test_put_and_get(self):
#        s = requests.session()
#        req = s.put("http://127.0.0.1:65430/put",data = """{
#                    "key":"sfs",
#                    "message":"1"
#                    }""")
#        req1 = s.get("http://127.0.0.1/get", data = """{
#            "key":"sfs"
#            }""")
#        print(req)
#        print(req1)
#
#    def test_put_del(self):
#        pass

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65430        # Port to listen on (non-privileged ports are > 1023)

hash = {}

appf = Flask(__name__)

logging.basicConfig(filename="sample.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',filemode = "w")

@appf.route("/get", methods = ["GET"])
def post():
    logging.debug("get for key [{}]".format(resp["key"]))
    resp = request.data.decode("utf-8")
    resp = json.loads(resp)
    try:
        datafrHash = hash[resp["key"]]
        return json.dumps({"status": "Ok", "message": datafrHash}).encode("utf-8")
    except KeyError:
        logging.warning("no data in cache for key [{}]".format(resp["key"]))
        return json.dumps({"status": "Not Found"}).encode("utf-8"), '404'
    except:
        return "Internal Server Error".encode("utf-8"), '403'

@appf.route("/delete", methods = ["DELETE"])
def delete():
    resp = request.data.decode("utf-8")
    resp = json.loads(resp)
    try:
        del hash[resp["key"]]
        return json.dumps({"status":"OK"}).encode("utf-8")
    except KeyError:
        return json.dumps({"status": "Not Found"}).encode("utf-8"), '404'
    except:
        return "Internal Server Error".encode("utf-8"), '403'

@appf.route("/put", methods = ["PUT"])
def put():
    resp = request.data.decode("utf-8")
    resp = json.loads(resp)
    try:
        hash[resp["key"]] = resp["message"]
        return json.dumps({"status":"Create"}).encode("utf-8")
    except:
        return "Internal Server Error".encode("utf-8"), '403'

if __name__ == '__main__':
    appf.run(host = HOST, port = PORT)
    unittest.main()
