# coding:utf8
import re
import json
import redis
import schedule
import datetime
import os
import time
import shutil

current_dir = '/Users/edz/Desktop/zhengmangProject/UpdateGdtCookies/'
# current_dir = '/work/update_gdtcookies/'
cookie_file_name = 'gdt_cookie.json'

class GdtBaseSpider:
    def __init__(self):
        # pool = redis.ConnectionPool(host='172.17.31.161', port=6379, db=3)
        pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=3)
        self.client = redis.Redis(connection_pool=pool)

    def save_cookie(self,custom_id,account_id,token):
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if token['cookie'] and token['tk']:
            try:
                owner = re.search(r".*uid=(.*)&g_tk.*", token['tk'], re.S).group(1)
                g_tk = re.search(r".*g_tk=(.*)&fans_code.*",token['tk'],re.S).group(1)#self.get_query_value(token['tk'], 'g_tk')
            except:
                owner = re.search(r".*owner=(.*)&advertiser_id.*", token['tk'], re.S).group(1)
                g_tk = re.search(r".*g_tk=(.*)&owner=.*", token['tk'], re.S).group(1)
            #atlas_platform=CPD  re.search(r'&%s=(.*?)&' % str, data_list, re.S).group(1)
            # atlas_platform = re.search(r"atlas_platform=(.*?)", token['cookie'], re.S).group(1)
            atlas_platform = token['cookie'].split(';')[-1].split('=')[1]
            # print('atlas_platform:{}'.format(atlas_platform))
            info = {}
            info["custom_id"] = custom_id
            info["g_tk"] = g_tk
            info["owner"] = owner
            info["atlas_platform"] = atlas_platform
            spider_info = json.loads(self.client.hmget("gdt_spiders", str(account_id))[0])
            list1 = token['cookie'].split(';')
            keys = []
            values = []
            for toup in list1:
                keys.append(toup.split('=')[0])
                values.append(toup.split('=')[1])
            cookies = dict(zip(keys, values))
            spider_info['cookies'] = cookies
            spider_info['info'] = info
            self.client.hset("gdt_spiders", account_id, json.dumps(spider_info))
            print(account_id)
            print(json.dumps(spider_info))
            print("保存成功!{}".format(now_time))
        else:
            print('保存失败!{}'.format(now_time))

    def is_exist_file(self,filename):
        file_path = current_dir + filename
        if os.path.exists(file_path):
            return True
        else:
            return False

    def read_jsonfile(self,filename):
        pass
        json_path = current_dir + filename
        with open(json_path,'r') as f:
            load_dict = json.load(f)
        return load_dict

    def start1(self):
        if self.is_exist_file(cookie_file_name):
            load_dict = self.read_jsonfile(cookie_file_name)
            results = load_dict['results']
            for dict1 in results:
                username = dict1['username']
                password = dict1['password']
                custom_id = dict1['custom_id']
                account_id = dict1['account_id']
                token = dict1['token']
                print(username, password,custom_id,account_id)
                self.save_cookie(custom_id, account_id,token)

def judge():
    # 判断当前目录是否有新的cookie文件生成
    # 把新生成的cookie文件更新到redis
    # 更新完cookie之后，把文件移走
    file_path = current_dir + cookie_file_name
    if os.path.exists(file_path):
        print('有新的文件生成')
        main()
        print('redis更新结束！')
        dstfile = current_dir + 'cookie_files/' + str(round(time.time() * 100)) + '.json'
        fpath, fname = os.path.split(dstfile)  # 分离文件名和路径
        print(fpath, fname)
        if not os.path.exists(fpath):
            os.makedirs(fpath)
        shutil.move(file_path, dstfile)
        print('{}移动成功！'.format(cookie_file_name))

def main():
    gdt_base_spider = GdtBaseSpider()
    gdt_base_spider.start1()

if __name__ == '__main__':
    # schedule.every().day.at("10:50").do(main)
    # schedule.every().day.at("11:53").do(main)
    schedule.every(0.01).minutes.do(judge)
    while True:
        schedule.run_pending()
    # main()
