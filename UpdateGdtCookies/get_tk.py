import time
import os
import re
import json
import requests
import shutil

cookie_mitmproxy = 'gdt_cookie_mitmproxy.txt'
cookie_ssh = 'gdt_cookie.json'
current_dir = '/Users/edz/Desktop/zhengmangProject/UpdateGdtCookies/'

def get_g_tk(url1):
    list1 = url1.split('?')
    args_list = list1[1].split('&')
    for item in args_list:
        if 'g_tk' in item:
            g_tk = item
        if 'owner' in item:
            owner = item
    tk = 'https://mp.e.qq.com/abc/qrcode?{}&{}&timestamp={}'.format(owner,g_tk,round(time.time() * 1000))
    return tk

def write_file():
    with open('gdt_cookie.txt','r') as f:
        lines = f.readlines()
    os.remove('gdt_cookie.txt')
    for line in lines:
        dict1 = eval(line)
        token = dict1['token']
        tk = token['tk']
        try:
            if 'uid'in tk:
                tk = tk.replace('uid','owner')
            else:
                tk = get_g_tk(tk)
        except:
            tk = tk
        token.update(tk=tk)
        dict1.update(token=token)
        print(dict1)
        with open('gdt_cookie.txt','a') as f:
            f.write(str(dict1)+'\n')

def format_json(usernames):
    list1 = []
    list2 = []
    with open(cookie_mitmproxy,'r') as f:
        lines = f.readlines()
    for line in lines:
        if 'g_tk' in line and 'owner' in line and 'ptui_loginuin' in line and 'atlas_platform' in line:
            dict1 = eval(line)
            url = dict1['url']
            cookies = dict1['cookies']
            url_list = url.split('?')[1].split('&')
            for item in url_list:
                if 'g_tk' in item:
                    g_tk = re.search(r".*g_tk=(.*)", item, re.S).group(1)
                if 'owner' in item:
                    owner = re.search(r".*owner=(.*)", item, re.S).group(1)
            ptui_loginuin = cookies['ptui_loginuin']
            atlas_platform = cookies['atlas_platform']
            gdt_token = cookies['gdt_token']
            gdt_protect = cookies['gdt_protect']
            str_cookie = "portalversion=new;atlas_platform={};gdt_token={};gdt_protect={}".format(atlas_platform, gdt_token,gdt_protect)
            if ptui_loginuin not in list1:
                list1.append(ptui_loginuin)
                for item in usernames:
                    username = item['username']
                    if ptui_loginuin == username:
                        tk = "https://mp.e.qq.com/abc/qrcode?uid={}&g_tk={}&fans_code=ATALS-2001&timestamp={}".format(owner,g_tk,str(round(time.time()*100)))
                        dict2 = {'cookie':str_cookie,'tk':tk}
                        item.update(code=200)
                        item.update(token=dict2)
                        list2.append(item)
                        print(item)
    dict1 = {'results': list2}
    json_dict = json.dumps(dict1, ensure_ascii=False, indent=4)
    with open(cookie_ssh, 'w', encoding='utf8') as f:
        f.write(json_dict)

def get_usernames():
    pass
    list1 = []
    mango_login_url = 'http://auto.mango-go.com/api/login'
    url = mango_login_url
    mango_login_username = 'spider'
    mango_login_password = '^JFiFY!$q1gh'
    body = {'username': mango_login_username, 'password': mango_login_password}
    res = requests.post(url, data=json.dumps(body))
    cookies = "token=%s;username=%s" % (res.cookies['token'], mango_login_username)
    header = {"cookie": cookies}
    res = requests.get(url='http://auto.mango-go.com/api/go/mediaAccount/queryAccountList', headers=header)
    account_infos = json.loads(res.text)
    data = account_infos['data']
    for item in data:
        if item['channelType'] == 'gdt' and item['status'] == '1':
            username = item['username']
            password = item['password']
            custom_id = item['customId']
            account_id = item['accountId']
            dict1 = {'username':username,'password':password,'custom_id':custom_id,'account_id':account_id}
            list1.append(dict1)
    print(len(list1))
    print(list1)
    return list1

if __name__ == '__main__':
    if os.path.exists(cookie_mitmproxy):
        print('{} is exit!'.format(cookie_mitmproxy))
        list1 = get_usernames()
        format_json(list1)
        srcfile = current_dir + 'gdt_cookie_mitmproxy.txt'
        dstfile = current_dir + 'cookie_files/' + str(round(time.time()*1000)) + '_gdt_cookie_mitmproxy.txt'
        fpath,fname = os.path.split(dstfile)
        if not os.path.exists(fpath):
            os.makedirs(fpath)
        shutil.move(srcfile,dstfile)
        print('{} move success!'.format(cookie_mitmproxy))

