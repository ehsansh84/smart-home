import os
import sys
import requests
from tools.log_tools import log
import string
import random
from datetime import datetime
from dotenv import load_dotenv
sys.path.append('/root/dev/app')
load_dotenv()
# print(os.getenv('MONGODB_HOST'))
# MONGODB_HOST = 'mongodb://localhost:27021'
# MONGODB_HOST = 'mongodb://mongodb'
# CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
# CELERY_BACKEND_URL = os.getenv('CELERY_BACKEND_URL')
# MONGO_URL = os.getenv('MONGO_URL')
# DB_NAME = os.getenv('DB_NAME')
MONGO_URL = 'mongodb://localhost:27017'
DB_NAME = 'smart'


def db():
    from pymongo import MongoClient
    log.debug(MONGO_URL)
    con = MongoClient(MONGO_URL, connectTimeoutMS=1000)
    return con[DB_NAME]


def print_exception():
    import linecache
    import sys
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    log.error('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))
    return 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)


def exception_line():
    import linecache
    import sys
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    return f"{filename}:{lineno} => {line.strip()}"


def serialize_dict(item):
    if item is None:
        return {}
    else:
        # return {**{'id': str(item[i]) for i in item if i == '_id'}, **{i: item[i] for i in item if i != '_id'}}
        return {**{'id': str(item[i]) for i in item if i == '_id' or isinstance(item[i], datetime)},
                **{i: item[i] for i in item if i != '_id' and not isinstance(item[i], datetime)}}


def serialize_list(items):
    return [serialize_dict(item) for item in items]
