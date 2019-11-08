# coding:utf8
from selenium.webdriver.common.action_chains import ActionChains
import requests
import json
import urllib3
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import shutil

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  #禁用requests安全建议警告，不影响结果

current_dir = '/Users/edz/Desktop/zhengmangProject/UpdateGdtCookies/'
# current_dir = '/work/update_gdtcookies/'
ssh_file_path = '/work/update_gdtcookies/gdt_cookie.json'
executable_path='/Users/edz/Desktop/chromedriver'

class GdtBaseSpider:
    def __init__(self):
        self.wait_time = 30
        self.cookie_file_name = 'gdt_cookie.json'
        self.refresh_time = 3

    def is_exist_file(self,filename):
        file_path = current_dir + filename
        if os.path.exists(file_path):
            return True
        else:
            return False

    def write_cookie(self,dict1):
        pass
        if self.is_exist_file(self.cookie_file_name):
            with open(self.cookie_file_name, 'r') as f:
                load_dict = json.load(f)
            results = load_dict['results']
            results.append(dict1)
            dict1 = {'results': results}
            json_dict = json.dumps(dict1, ensure_ascii=False, indent=4)
            with open(self.cookie_file_name, 'w', encoding='utf8') as f:
                f.write(json_dict)
        else:
            dict1 = {'results':[dict1]}
            json_dict = json.dumps(dict1, ensure_ascii=False, indent=4)
            with open(self.cookie_file_name, 'w', encoding='utf8') as f:
                f.write(json_dict)

    def func_js2(self,uuid1):
        import execjs
        js_str = """
        function get_tk(e) {
                var t = 5381;
                e = e || n();
                for (var o = 0, r = e.length; o < r; ++o) {
                    t += (t << 5) + e.charAt(o).charCodeAt()
                }
                return t & 2147483647
            };
        """
        ctx = execjs.compile(js_str)
        g_tk = ctx.call('get_tk', uuid1)  # "1963070c7273e0559025f79984db257f7654ab7d")
        print(g_tk)
        return g_tk

    def login_qq(self,username, password, custom_id, account_id):
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument("--proxy-server=http://121.206.141.74:18176")
        driver = webdriver.Chrome(executable_path=executable_path)#,chrome_options=chromeOptions)
        driver.implicitly_wait(10)
        driver.maximize_window()
        driver.get('https://e.qq.com/ads/')
        wait = WebDriverWait(driver,10)
        driver.find_element_by_xpath('//*[@id="loginBtn"]').click()  # 登陆
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID,'ptlogin_iframe')))
        driver.find_element_by_xpath('//*[@id="switcher_plogin"]').click()  # 账号密码登陆
        driver.find_element_by_xpath('//*[@id="u"]').send_keys(username)  # 输入QQ号码
        driver.find_element_by_xpath('//*[@id="p"]').send_keys(password)  # 输入密码
        driver.find_element_by_xpath('//*[@id="login_button"]').click()  # 点击登陆
        time.sleep(self.wait_time)  # 可能会出现滑块或者扫码
        try:
            ele = driver.find_element_by_xpath('//*[@id="userinfoTxImg"]')  # 鼠标移到悬停元素上
            ActionChains(driver).move_to_element(ele).perform()
            driver.find_element_by_xpath('//*[@id="in-manage-btn"]').click()  # 进入投放管理平台
            if custom_id == None:
                try:
                    # 代理商页面，首页显示的有广告投放，点击进入子页面
                    handler1 = driver.current_window_handle
                    driver.find_element_by_xpath('//tbody[@class="spa-ui"]/tr/td[8]/span/a').click() # 广告投放
                    handlers = driver.window_handles
                    for handler in handlers:
                        if handler1 != handler:
                            driver.switch_to.window(handler)
                    driver.refresh()
                    time.sleep(self.refresh_time)
                    cookie = driver.get_cookies()
                    print(cookie)
                    for l in cookie:
                        if l['name'] == 'atlas_platform':
                            atlas_platform = l['value']
                        if l['name'] == 'dm_cookie':
                            dm_cookie = l['value'] #onwer
                        if l['name'] == 'gdt_token':
                            gdt_token = l['value']
                        if l['name'] == 'gdt_protect':
                            gdt_protect = l['value'] #g_tk
                    str_cookie = "portalversion=new;atlas_platform={};gdt_token={};gdt_protect={}".format(atlas_platform,gdt_token,gdt_protect)
                    uid = dm_cookie.split('&')[-1].split('=')[-1]
                    g_tk = self.func_js2(gdt_protect)
                    tk = '//mp.e.qq.com/abc/qrcode?uid={}&g_tk={}&fans_code=ATALS-2001&timestamp=1569217024987'.format(uid,g_tk)
                    dict1 = {'code': 200, 'username': username, 'password': password, 'custom_id': custom_id,'account_id': account_id, 'token': {'cookie': str_cookie, 'tk': tk}}
                    self.write_cookie(dict1)
                    print('{},{},{},{}成功登陆'.format(username, password, custom_id, account_id))
                    driver.close()
                    driver.quit()
                    return
                except:
                    pass
                driver.refresh()
                time.sleep(self.refresh_time)
                cookie = driver.get_cookies()
                print(cookie)
                for l in cookie:
                    if l['name'] == 'atlas_platform':
                        atlas_platform = l['value']
                    if l['name'] == 'dm_cookie':
                        dm_cookie = l['value']  # onwer
                    if l['name'] == 'gdt_token':
                        gdt_token = l['value']
                    if l['name'] == 'gdt_protect':
                        gdt_protect = l['value']  # g_tk
                str_cookie = "portalversion=new;atlas_platform={};gdt_token={};gdt_protect={}".format(atlas_platform,gdt_token,gdt_protect)
                uid = dm_cookie.split('&')[-1].split('=')[-1]
                g_tk = self.func_js2(gdt_protect)
                tk = '//mp.e.qq.com/abc/qrcode?uid={}&g_tk={}&fans_code=ATALS-2001&timestamp=1569217024987'.format(uid,g_tk)
                dict1 = {'code': 200, 'username': username, 'password': password, 'custom_id': custom_id,'account_id': account_id, 'token': {'cookie': str_cookie, 'tk': tk}}
                self.write_cookie(dict1)
                print('{},{},{},{}成功登陆'.format(username, password, custom_id, account_id))
                driver.close()
                driver.quit()
                return
            if custom_id != None:
                login_handler = driver.current_window_handle
                new_url = 'https://e.qq.com/atlas/' + custom_id
                js = 'window.open("{}/");'.format(new_url)
                driver.execute_script(js)
                handlers = driver.window_handles
                for handler in handlers:
                    if handler != login_handler:
                        driver.switch_to.window(handler)
                driver.refresh()
                time.sleep(self.refresh_time)
                cookie = driver.get_cookies()
                for l in cookie:
                    if l['name'] == 'atlas_platform':
                        atlas_platform = l['value']
                    if l['name'] == 'dm_cookie':
                        dm_cookie = l['value']  # onwer
                    if l['name'] == 'gdt_token':
                        gdt_token = l['value']
                    if l['name'] == 'gdt_protect':
                        gdt_protect = l['value']  # g_tk
                str_cookie = "portalversion=new;atlas_platform={};gdt_token={};gdt_protect={}".format(atlas_platform,gdt_token,gdt_protect)
                g_tk = self.func_js2(gdt_protect)
                tk = '//mp.e.qq.com/abc/qrcode?uid={}&g_tk={}&fans_code=ATALS-2001&timestamp=1569217024987'.format(custom_id,g_tk)
                dict1 = {'code': 200, 'username': username, 'password': password, 'custom_id': custom_id,
                         'account_id': account_id, 'token': {'cookie': str_cookie, 'tk': tk}}
                self.write_cookie(dict1)
                print('{},{},{},{}成功登陆'.format(username, password, custom_id, account_id))
                # driver.close()
                # driver.quit()
                return
        except Exception as e:
            dict1 = {'code': 600, 'username': username, 'password': password, 'custom_id': custom_id,'account_id': account_id, 'token': {'cookie': None, 'tk': None}}
            self.write_cookie(dict1)
            print("{},{},{},{}登陆失败！".format(username, password, custom_id, account_id))
            driver.close()
            driver.quit()

    def send_ssh(self):
        import paramiko  # 此模块用于连接虚拟机,ansible底层用此模块
        hostname = '47.95.120.23'
        port = 22
        username = 'zmwork'
        password = 'ab&C2S8$14Xr#s0o'
        t = paramiko.Transport((hostname, port))
        t.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        cookie_file_path = current_dir + 'gdt_cookie.json'
        sftp.put(cookie_file_path, ssh_file_path)
        sftp.close()
        print('gdt_cookie.json成功上传！')

    def get_info(self):
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
        print('account_infos:{}'.format(account_infos))
        json_path = current_dir + 'info.json'
        json_dict = json.dumps(account_infos,ensure_ascii=False,indent=4)
        with open(json_path,'w',encoding='utf8') as f:
            f.write(json_dict)

    def read_jsonfile(self,filename):
        pass
        json_path = current_dir + filename
        with open(json_path,'r') as f:
            load_dict = json.load(f)
        return load_dict

    def move_file(self):
        srcfile = current_dir + 'gdt_cookie.json'
        dstfile = current_dir + 'cookie_files/' + str(round(time.time()*100)) + '.json'
        if not os.path.isfile(srcfile):
            print("%s not exist!" % (srcfile))
        else:
            fpath, fname = os.path.split(dstfile)  # 分离文件名和路径
            if not os.path.exists(fpath):
                os.makedirs(fpath)
            shutil.move(srcfile, dstfile)

    def start1(self):
        pass
        try:
            self.move_file()
        except:
            pass
        self.get_info()
        load_dict = self.read_jsonfile('info.json')
        data = load_dict['data']
        for dict1 in data:
            if dict1['channelType'] == 'gdt' and dict1['status'] == '1':
                # with open('gdt.txt','a') as f:
                #     f.write(str(dict1)+'\n')
                # print(dict1)
                username = dict1['username']
                password = dict1['password']
                custom_id = dict1['customId']
                account_id = dict1['accountId']
                if username in ['1350979618']:
                    if username == '3228705757':
                        custom_id = '2677129'
                    print(username, password, custom_id, account_id,'开始登陆！')
                    self.login_qq(username,password,custom_id,account_id)
        self.send_ssh()

if __name__ == '__main__':
    gdt_base_spider = GdtBaseSpider()
    gdt_base_spider.start1()
#getcampaignmultidimensionlist
#tsa_pgv_ssid=tsassid__1569210933232_496820509; tsa_pgv_pvid=tsapvid__1569210933233_115804281; site_type=new; portalversion=new; pgv_pvi=6686726144; pgv_si=s2090824704; __root_domain_v=.e.qq.com; _qddaz=QD.weiosq.yetopn.k0vvoa4t; _qddamta_2852155024=3-0; pgv_info=ssid=s6909334700; pgv_pvid=8699101136; gr_user_id=c07ef690-dd1d-4111-9989-4e9d651d01ab; gr_session_id_8751e4ce852fb210=fcee6fe4-6f34-44d4-9a50-d2ec25ab7d91; hottag=login; hottagtype=header; ptisp=cnc; ptui_loginuin=2906823864; RK=kDY9a9UouN; ptcz=d7cb6318832879328fa9e23f8c7e3c60fffe888a6a46dea74490b4ec44801651; gdt_refer=graph.qq.com; gdt_full_refer=https%3A%2F%2Fgraph.qq.com%2Foauth2.0%2Fshow%3Fwhich%3DLogin%26display%3Dpc%26response_type%3Dcode%26client_id%3D101477621%26redirect_uri%3Dhttps%253A%252F%252Fsso.e.qq.com%252Fpassport%253Fsso_redirect_uri%253Dhttps%25253A%25252F%25252Fe.qq.com%25252Fads%25252F%2526service_tag%253D1%26scope%3Dget_user_info; gdt_original_refer=graph.qq.com; gdt_original_full_refer=https%3A%2F%2Fgraph.qq.com%2Foauth2.0%2Fshow%3Fwhich%3DLogin%26display%3Dpc%26response_type%3Dcode%26client_id%3D101477621%26redirect_uri%3Dhttps%253A%252F%252Fsso.e.qq.com%252Fpassport%253Fsso_redirect_uri%253Dhttps%25253A%25252F%25252Fe.qq.com%25252Fads%25252F%2526service_tag%253D1%26scope%3Dget_user_info; gdt_token=TGT-18305-KyP53peZk46WI6FSP6p.3bJ65T2t6XqGYu.9e5Vrn3mdBEDmGWoME8sWhGzd5POi; gdt_protect=1f67435d60a617248fa2754ad1f4d7e587278071; _qdda=3-1.msh2y; _qddab=3-15xugw.k0vvov46; dm_cookie=version=new&log_type=internal_click&ssid=tsassid__1569210933232_496820509&pvid=tsapvid__1569210933233_115804281&qq=&loadtime=2253&url=https%3A%2F%2Fe.qq.com%2Fads%2F%3F&gdt_refer=graph.qq.com&gdt_full_refer=https%3A%2F%2Fgraph.qq.com%2Foauth2.0%2Fshow%3Fwhich%3DLogin%26display%3Dpc%26response_type%3Dcode%26client_id%3D101477621%26redirect_uri%3Dhttps%253A%252F%252Fsso.e.qq.com%252Fpassport%253Fsso_redirect_uri%253Dhttps%25253A%25252F%25252Fe.qq.com%25252Fads%25252F%2526service_tag%253D1%26scope%3Dget_user_info&gdt_original_refer=graph.qq.com&gdt_original_full_refer=https%3A%2F%2Fgraph.qq.com%2Foauth2.0%2Fshow%3Fwhich%3DLogin%26display%3Dpc%26response_type%3Dcode%26client_id%3D101477621%26redirect_uri%3Dhttps%253A%252F%252Fsso.e.qq.com%252Fpassport%253Fsso_redirect_uri%253Dhttps%25253A%25252F%25252Fe.qq.com%25252Fads%25252F%2526service_tag%253D1%26scope%3Dget_user_info&gdt_from=&uid=9797810; atlas_platform=atlas
#uid=tsa_pgv_ssid=tsassid__1569210933232_496820509; tsa_pgv_pvid=tsapvid__1569210933233_115804281; site_type=new; portalversion=new; pgv_pvi=6686726144; pgv_si=s2090824704; __root_domain_v=.e.qq.com; _qddaz=QD.weiosq.yetopn.k0vvoa4t; _qddamta_2852155024=3-0; pgv_info=ssid=s6909334700; pgv_pvid=8699101136; gr_user_id=c07ef690-dd1d-4111-9989-4e9d651d01ab; gr_session_id_8751e4ce852fb210=fcee6fe4-6f34-44d4-9a50-d2ec25ab7d91; hottag=login; hottagtype=header; ptisp=cnc; ptui_loginuin=2906823864; RK=kDY9a9UouN; ptcz=d7cb6318832879328fa9e23f8c7e3c60fffe888a6a46dea74490b4ec44801651; gdt_refer=graph.qq.com; gdt_full_refer=https%3A%2F%2Fgraph.qq.com%2Foauth2.0%2Fshow%3Fwhich%3DLogin%26display%3Dpc%26response_type%3Dcode%26client_id%3D101477621%26redirect_uri%3Dhttps%253A%252F%252Fsso.e.qq.com%252Fpassport%253Fsso_redirect_uri%253Dhttps%25253A%25252F%25252Fe.qq.com%25252Fads%25252F%2526service_tag%253D1%26scope%3Dget_user_info; gdt_original_refer=graph.qq.com; gdt_original_full_refer=https%3A%2F%2Fgraph.qq.com%2Foauth2.0%2Fshow%3Fwhich%3DLogin%26display%3Dpc%26response_type%3Dcode%26client_id%3D101477621%26redirect_uri%3Dhttps%253A%252F%252Fsso.e.qq.com%252Fpassport%253Fsso_redirect_uri%253Dhttps%25253A%25252F%25252Fe.qq.com%25252Fads%25252F%2526service_tag%253D1%26scope%3Dget_user_info; gdt_token=TGT-18305-KyP53peZk46WI6FSP6p.3bJ65T2t6XqGYu.9e5Vrn3mdBEDmGWoME8sWhGzd5POi; gdt_protect=1f67435d60a617248fa2754ad1f4d7e587278071; _qdda=3-1.msh2y; _qddab=3-15xugw.k0vvov46; dm_cookie=version=new&log_type=internal_click&ssid=tsassid__1569210933232_496820509&pvid=tsapvid__1569210933233_115804281&qq=&loadtime=2253&url=https%3A%2F%2Fe.qq.com%2Fads%2F%3F&gdt_refer=graph.qq.com&gdt_full_refer=https%3A%2F%2Fgraph.qq.com%2Foauth2.0%2Fshow%3Fwhich%3DLogin%26display%3Dpc%26response_type%3Dcode%26client_id%3D101477621%26redirect_uri%3Dhttps%253A%252F%252Fsso.e.qq.com%252Fpassport%253Fsso_redirect_uri%253Dhttps%25253A%25252F%25252Fe.qq.com%25252Fads%25252F%2526service_tag%253D1%26scope%3Dget_user_info&gdt_original_refer=graph.qq.com&gdt_original_full_refer=https%3A%2F%2Fgraph.qq.com%2Foauth2.0%2Fshow%3Fwhich%3DLogin%26display%3Dpc%26response_type%3Dcode%26client_id%3D101477621%26redirect_uri%3Dhttps%253A%252F%252Fsso.e.qq.com%252Fpassport%253Fsso_redirect_uri%253Dhttps%25253A%25252F%25252Fe.qq.com%25252Fads%25252F%2526service_tag%253D1%26scope%3Dget_user_info&gdt_from=&uid=9797810; atlas_platform=atlas
#yeah201207