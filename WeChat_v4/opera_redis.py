import redis
import time

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

# if __name__ == '__main__':
#     while True:
#         keys = get_keys()
#         for key in keys:
#             if keys:
#                 print(key)
#                 if keys:
#                     values = get_values(key)
#                     print(values)
#                     del_key(key)