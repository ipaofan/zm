#encoding:utf8
from concurrent.futures import ThreadPoolExecutor
from wxpy import *
import time
from utils import write_log,get_keys,get_values,del_key

bot = Bot(cache_path=True)
test_name = '诸葛飞飞'
def keep_concent():
    while True:
        my_friend = bot.friends().search(test_name)[0]
        my_friend.send('test message:keep connect!')
        time.sleep(60 * 10)

def name_isexit():
    while True:
        keys = get_keys()
        for key in keys:
            dict1 = get_values(key)
            write_log(str(dict1))
            try:
                copywriting = dict1[b'copywriting'].decode('utf-8')
                rooms = [dict1[b'room'].decode('utf-8')]
            except:
                pass
            try:
                photo_path = dict1[b'photo_path'].decode('utf-8')
                if photo_path:
                    send_photo(copywriting, photo_path,rooms)
                    del_key(key)
            except:
                pass
            try:
                text = dict1[b'text'].decode('utf-8')
                if text:
                    send_text(copywriting, text,rooms)
                    del_key(key)
            except:
                pass
            time.sleep(60)


def send_photo(copywriting,photo_path,rooms):
    my_friend = bot.friends().search(test_name)[0]
    my_friend.send(copywriting)
    my_friend.send_image(photo_path)

    groups = bot.groups()
    my_group = groups.search(rooms[0])[0]
    my_group.send(copywriting)
    my_group.send('@img@{}'.format(photo_path))
    print('send photo success!')
    write_log('send photo success!')



def send_text(copywriting,text,rooms):
    my_friend = bot.friends().search(test_name)[0]
    my_friend.send(copywriting)
    my_friend.send(text)

    groups = bot.groups()
    my_group = groups.search(rooms[0])[0]
    my_group.send(copywriting)
    my_group.send(text)
    print('send text success!')
    write_log('send text success!')

if __name__ == '__main__':
    pool = ThreadPoolExecutor(max_workers=2)
    pool.submit(keep_concent)
    pool.submit(name_isexit)