import redis
import json
import schedule

def get_info():
    pool = redis.ConnectionPool(host='172.17.31.161', port=6379, db=3)
    client = redis.Redis(connection_pool=pool)
    ad_channels = ['baidu_sem', 'baidu_feed', 'sougou_sem', 'gdt', 'yixiao', 'toutiao', 'shenma_sem']
    account_info_list = []
    for channelType in ad_channels:
        keys = client.hkeys("%s_spiders" % channelType)
        for account_info in client.hmget("%s_spiders" % channelType, keys):
            account_info = json.loads(account_info)
            if account_info['status'] == '1':
                print(account_info)
                account_info_list.append(account_info)
    account_info_dict = {'retcode':200,"retdesc": "成功",'data':account_info_list}
    json_dict = json.dumps(account_info_dict, ensure_ascii=False, indent=4)
    with open("info.json","w",encoding='utf8') as f:
        f.write(json_dict)
        print("加载入文件完成...")

if __name__ == '__main__':
    schedule.every().day.at("12:00").do(get_info)
    while True:
        schedule.run_pending()
    # get_info()