import logging
import time
from config import current_dir
import os

log_dir = current_dir + 'logs/'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

def write_log(content):
    filename = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s \tFile \"%(filename)s\"[line:%(lineno)d] %(levelname)s %(message)s',
                            # datefmt='%a, %d %b %Y %H:%M:%S',
                            filename=current_dir + "/logs/" + filename + ".log",
                            filemode='a')

    # logging.debug('debug message')
    logging.info(content)
    # logging.warn('warn message')
    # logging.error('error message')
    # logging.critical('critical message')



import redis

pool = redis.ConnectionPool(host='localhost', port=6379,db=9)
red = redis.Redis(connection_pool=pool)

def insert_redis(dict1):
    red.hmset(str(round(time.time() * 1000)),dict1)

def get_values(name):
    return red.hgetall(name)

def get_keys():
    return red.keys()

def del_key(name):
    red.delete(name)