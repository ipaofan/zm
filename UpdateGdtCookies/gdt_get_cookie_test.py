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
from urllib import request
import cv2
import numpy as np

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  #禁用requests安全建议警告，不影响结果

current_dir = '/Users/edz/Desktop/zhengmangProject/UpdateGdtCookies/'
# current_dir = '/work/update_gdtcookies/'
ssh_file_path = '/work/update_gdtcookies/gdt_cookie.json'
executable_path='/Users/edz/Desktop/chromedriver'

class GdtBaseSpider:
    def __init__(self):
        self.wait_time = 3
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
            driver.find_element_by_xpath('//*[@id="login_button"]').click()  # 点击登陆
        except:
            pass
        self.drag_slide(driver)
        driver.close()
        driver.quit()

        # try:
        #     ele = driver.find_element_by_xpath('//*[@id="userinfoTxImg"]')  # 鼠标移到悬停元素上
        #     ActionChains(driver).move_to_element(ele).perform()
        #     driver.find_element_by_xpath('//*[@id="in-manage-btn"]').click()  # 进入投放管理平台
        #     if custom_id == None:
        #         try:
        #             # 代理商页面，首页显示的有广告投放，点击进入子页面
        #             handler1 = driver.current_window_handle
        #             driver.find_element_by_xpath('//tbody[@class="spa-ui"]/tr/td[8]/span/a').click() # 广告投放
        #             handlers = driver.window_handles
        #             for handler in handlers:
        #                 if handler1 != handler:
        #                     driver.switch_to.window(handler)
        #             driver.refresh()
        #             time.sleep(self.refresh_time)
        #             cookie = driver.get_cookies()
        #             print(cookie)
        #             for l in cookie:
        #                 if l['name'] == 'atlas_platform':
        #                     atlas_platform = l['value']
        #                 if l['name'] == 'dm_cookie':
        #                     dm_cookie = l['value'] #onwer
        #                 if l['name'] == 'gdt_token':
        #                     gdt_token = l['value']
        #                 if l['name'] == 'gdt_protect':
        #                     gdt_protect = l['value'] #g_tk
        #             str_cookie = "portalversion=new;atlas_platform={};gdt_token={};gdt_protect={}".format(atlas_platform,gdt_token,gdt_protect)
        #             uid = dm_cookie.split('&')[-1].split('=')[-1]
        #             g_tk = self.func_js2(gdt_protect)
        #             tk = '//mp.e.qq.com/abc/qrcode?uid={}&g_tk={}&fans_code=ATALS-2001&timestamp=1569217024987'.format(uid,g_tk)
        #             dict1 = {'code': 200, 'username': username, 'password': password, 'custom_id': custom_id,'account_id': account_id, 'token': {'cookie': str_cookie, 'tk': tk}}
        #             self.write_cookie(dict1)
        #             print('{},{},{},{}成功登陆'.format(username, password, custom_id, account_id))
        #             driver.close()
        #             driver.quit()
        #             return
        #         except:
        #             pass
        #         driver.refresh()
        #         time.sleep(self.refresh_time)
        #         cookie = driver.get_cookies()
        #         print(cookie)
        #         for l in cookie:
        #             if l['name'] == 'atlas_platform':
        #                 atlas_platform = l['value']
        #             if l['name'] == 'dm_cookie':
        #                 dm_cookie = l['value']  # onwer
        #             if l['name'] == 'gdt_token':
        #                 gdt_token = l['value']
        #             if l['name'] == 'gdt_protect':
        #                 gdt_protect = l['value']  # g_tk
        #         str_cookie = "portalversion=new;atlas_platform={};gdt_token={};gdt_protect={}".format(atlas_platform,gdt_token,gdt_protect)
        #         uid = dm_cookie.split('&')[-1].split('=')[-1]
        #         g_tk = self.func_js2(gdt_protect)
        #         tk = '//mp.e.qq.com/abc/qrcode?uid={}&g_tk={}&fans_code=ATALS-2001&timestamp=1569217024987'.format(uid,g_tk)
        #         dict1 = {'code': 200, 'username': username, 'password': password, 'custom_id': custom_id,'account_id': account_id, 'token': {'cookie': str_cookie, 'tk': tk}}
        #         self.write_cookie(dict1)
        #         print('{},{},{},{}成功登陆'.format(username, password, custom_id, account_id))
        #         driver.close()
        #         driver.quit()
        #         return
        #     if custom_id != None:
        #         login_handler = driver.current_window_handle
        #         new_url = 'https://e.qq.com/atlas/' + custom_id
        #         js = 'window.open("{}/");'.format(new_url)
        #         driver.execute_script(js)
        #         handlers = driver.window_handles
        #         for handler in handlers:
        #             if handler != login_handler:
        #                 driver.switch_to.window(handler)
        #         driver.refresh()
        #         time.sleep(self.refresh_time)
        #         cookie = driver.get_cookies()
        #         for l in cookie:
        #             if l['name'] == 'atlas_platform':
        #                 atlas_platform = l['value']
        #             if l['name'] == 'dm_cookie':
        #                 dm_cookie = l['value']  # onwer
        #             if l['name'] == 'gdt_token':
        #                 gdt_token = l['value']
        #             if l['name'] == 'gdt_protect':
        #                 gdt_protect = l['value']  # g_tk
        #         str_cookie = "portalversion=new;atlas_platform={};gdt_token={};gdt_protect={}".format(atlas_platform,gdt_token,gdt_protect)
        #         g_tk = self.func_js2(gdt_protect)
        #         tk = '//mp.e.qq.com/abc/qrcode?uid={}&g_tk={}&fans_code=ATALS-2001&timestamp=1569217024987'.format(custom_id,g_tk)
        #         dict1 = {'code': 200, 'username': username, 'password': password, 'custom_id': custom_id,
        #                  'account_id': account_id, 'token': {'cookie': str_cookie, 'tk': tk}}
        #         self.write_cookie(dict1)
        #         print('{},{},{},{}成功登陆'.format(username, password, custom_id, account_id))
        #         return
        # except Exception as e:
        #     dict1 = {'code': 600, 'username': username, 'password': password, 'custom_id': custom_id,'account_id': account_id, 'token': {'cookie': None, 'tk': None}}
        #     self.write_cookie(dict1)
        #     print("{},{},{},{}登陆失败！".format(username, password, custom_id, account_id))
        #     driver.close()
        #     driver.quit()

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

    def drag_slide(self,driver):
        try:
            time.sleep(0.5)
            driver.switch_to.frame('ptlogin_iframe')
            time.sleep(0.5)
            driver.switch_to.frame('tcaptcha_iframe')
            time.sleep(0.5)
            # 用于找到登录图片的大图
            bigimg = driver.find_element_by_xpath('//img[@id="slideBg"]').get_attribute("src")
            # 用来找到登录图片的小滑块
            smallimg = driver.find_element_by_xpath('//img[@id="slideBlock"]').get_attribute("src")
            # 背景大图命名
            backimg = current_dir + "backimg.png"
            # 滑块命名
            slideimg = current_dir + "slideimg.png"
            # 下载背景大图保存到本地
            request.urlretrieve(bigimg, backimg)
            # 下载滑块保存到本地
            request.urlretrieve(smallimg, slideimg)
            # 获取图片并灰度化
            block = cv2.imread(slideimg, 0)
            template = cv2.imread(backimg, 0)
            # 二值化后的图片名称
            blockName = current_dir + "block.jpg"
            templateName = current_dir + "template.jpg"
            # 将二值化后的图片进行保存
            cv2.imwrite(blockName, block)
            cv2.imwrite(templateName, template)
            block = cv2.imread(blockName)
            block = cv2.cvtColor(block, cv2.COLOR_RGB2GRAY)
            block = abs(255 - block)
            cv2.imwrite(blockName, block)
            block = cv2.imread(blockName)
            template = cv2.imread(templateName)
            # 获取偏移量
            result = cv2.matchTemplate(block, template, cv2.TM_CCOEFF_NORMED)  # 查找block在template中的位置，返回result是一个矩阵，是每个点的匹配结果
            x, y = np.unravel_index(result.argmax(), result.shape)
            print('x:{},y:{}'.format(x,y))
            tracks = self.get_tracks1(y)
            button = driver.find_element_by_xpath('//img[@id="slideBlock"]')
            ActionChains(driver).click_and_hold(button).perform()
            for track in tracks:
                ActionChains(driver).move_by_offset(xoffset=track, yoffset=0).perform()
            time.sleep(0.18)
            # 反向滑动
            # for back in tracks_backs:
            #      ActionChains(self.dr).move_by_offset(xoffset=back, yoffset=0).perform()
            ActionChains(driver).move_by_offset(xoffset=-3, yoffset=0).perform()
            ActionChains(driver).move_by_offset(xoffset=3, yoffset=0).perform()
            time.sleep(0.7)
            ActionChains(driver).release().perform()
            time.sleep(1)
        except BaseException as e:
            print(e)

    def get_tracks1(self,distance):
        tracks = []
        current = 0
        # 其实64这个值大概准确有时出错，因为他滑块其实位置可能会有偏差，所以下面重新调用多次尝试
        while current < distance:
            tracks.append(3)
            current += 3
        return tracks

    def start1(self):
        try:
            self.move_file()
        except BaseException as e:
            print(e)
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
                if username not in []:
                    if username == '3228705757':
                        custom_id = '2677129'
                    print(username, password, custom_id, account_id,'开始登陆！')
                    self.login_qq(username,password,custom_id,account_id)
        # self.send_ssh()

if __name__ == '__main__':
    gdt_base_spider = GdtBaseSpider()
    gdt_base_spider.start1()
