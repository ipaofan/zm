import time
from wxpy import *

bot = Bot(cache_path=True)

while True:
    my_friend = bot.friends().search('诸葛飞飞')[0]
    my_friend.send('Hello friend')
    my_friend.send_image('/Users/edz/Desktop/zhengmangProject/WeChat_v4/photos/1569378380810.jpg')

    groups=bot.groups()
    my_group = groups.search('测试2')[0]
    my_group.send("好，这是测试程序发的信息")
    my_group.send('@img@/Users/edz/Desktop/zhengmangProject/WeChat_v4/photos/1569378380810.jpg')
    print('success!')
    time.sleep(60*6)