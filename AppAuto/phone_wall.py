# -*- encoding=utf8 -*-
__author__ = "edz"
import multiprocessing
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from airtest.core.api import *
import time
from concurrent.futures import ThreadPoolExecutor
import threading

class PhoneWall():
    def __init__(self):
        self.wait_time = 3
        self.loop_num = 10000

    def vivo_usb(self):
        device_1 = connect_device('android:339b19f1')  # vivo
        poco = AndroidUiautomationPoco(device=device_1, use_airtest_input=True, screenshot_each_action=False)
        # for i in range(self.loop_num):
        #     print('{}_vivo_usb'.format(i))
        #     # 首页
        #     poco("android.widget.LinearLayout").offspring("android:id/tabs").child("android.widget.RelativeLayout")[
        #         0].child("com.ss.android.article.lite:id/axy").click()
        #     poco("android.widget.LinearLayout").offspring("android:id/tabs").child("android.widget.RelativeLayout")[
        #         0].child("com.ss.android.article.lite:id/axy").click()
        #     time.sleep(10)
        #     poco.swipe([0.5, 0.8], [0.5, 0.2])
        #     time.sleep(10)
        #     # 视频
        #     poco("android.widget.LinearLayout").offspring("android:id/tabs").child("android.widget.RelativeLayout")[
        #         1].child("com.ss.android.article.lite:id/axy").click()
        #     poco("android.widget.LinearLayout").offspring("android:id/tabs").child("android.widget.RelativeLayout")[
        #         1].child("com.ss.android.article.lite:id/axy").click()
        #     time.sleep(10)
        #     poco.swipe([0.5, 0.8], [0.5, 0.2])
        #     time.sleep(10)
        #     # 评论
        #     poco("com.ss.android.article.lite:id/ank").click()
        #     time.sleep(20)
        #     # 返回
        #     poco("com.ss.android.article.lite:id/aid").click()
        self.trail1(poco,'vivo_usb')

    def xiaomi_usb(self):
        device_2 = connect_device('android:c4e6cc907d25')
        poco = AndroidUiautomationPoco(device=device_2, use_airtest_input=True, screenshot_each_action=False)
        # for i in range(self.loop_num):
        #     print('{}_xiaomi_usb'.format(i))
        #     # 首页
        #     poco("android.widget.LinearLayout").offspring("android:id/tabs").child("android.widget.RelativeLayout")[
        #         0].child("com.ss.android.article.lite:id/axy").click()
        #     poco("android.widget.LinearLayout").offspring("android:id/tabs").child("android.widget.RelativeLayout")[
        #         0].child("com.ss.android.article.lite:id/axy").click()
        #     time.sleep(10)
        #     poco.swipe([0.5, 0.8], [0.5, 0.2])
        #     time.sleep(10)
        #     # 视频
        #     poco("android.widget.LinearLayout").offspring("android:id/tabs").child("android.widget.RelativeLayout")[
        #         1].child("com.ss.android.article.lite:id/axy").click()
        #     poco("android.widget.LinearLayout").offspring("android:id/tabs").child("android.widget.RelativeLayout")[
        #         1].child("com.ss.android.article.lite:id/axy").click()
        #     time.sleep(10)
        #     poco.swipe([0.5, 0.8], [0.5, 0.2])
        #     time.sleep(10)
        #     # 评论
        #     poco("com.ss.android.article.lite:id/ank").click()
        #     time.sleep(20)
        #     # 返回
        #     poco("com.ss.android.article.lite:id/aid").click()
        self.trail1(poco,'xiaomi_usb')

    def huawei_usb(self):
        device_2 = connect_device('android:T7G0215804000411')
        poco = AndroidUiautomationPoco(device=device_2, use_airtest_input=True, screenshot_each_action=False)
        self.trail1(poco,'huawei_usb')

    def oppo_usb(self):
        #UOI7NVMN99999999
        device_2 = connect_device('android:UOI7NVMN99999999')
        poco = AndroidUiautomationPoco(device=device_2, use_airtest_input=True, screenshot_each_action=False)
        self.trail1(poco, 'oppo_usb')

    def vivo_wifi(self):
        device_1 = connect_device('android:///192.168.103.156:48887?cap_method=javacap&touch_method=adb')
        poco = AndroidUiautomationPoco(device=device_1, use_airtest_input=True, screenshot_each_action=False)
        self.trail1(poco, 'vivo_wifi')

    def xiaomi_wifi(self):
        device_1 = connect_device('android:///192.168.102.178:48887?cap_method=javacap&touch_method=adb')
        poco = AndroidUiautomationPoco(device=device_1, use_airtest_input=True, screenshot_each_action=False)
        self.trail1(poco,'xiaomi_wifi')

    def huawei_wifi(self):
        device_1 = connect_device('android:///192.168.103.253:48887?cap_method=javacap&touch_method=adb')
        poco = AndroidUiautomationPoco(device=device_1, use_airtest_input=True, screenshot_each_action=False)
        self.trail1(poco, 'huawei_wifi')

    def oppo_wifi(self):
        device_1 = connect_device('android:///192.168.102.71:48887?cap_method=javacap&touch_method=adb')
        poco = AndroidUiautomationPoco(device=device_1, use_airtest_input=True, screenshot_each_action=False)
        self.trail1(poco, 'oppo_wifi')

    def trail1(self,poco,phone_name):
        for i in range(self.loop_num):
            print('{}_{}'.format(i,phone_name))
            # 首页
            # poco("android.widget.LinearLayout").offspring("android:id/tabs").child("android.widget.RelativeLayout")[
            #     0].child("com.ss.android.article.lite:id/axy").click()
            # poco("android.widget.LinearLayout").offspring("android:id/tabs").child("android.widget.RelativeLayout")[
            #     0].child("com.ss.android.article.lite:id/axy").click()
            # time.sleep(self.wait_time)
            poco.swipe([0.5, 0.2], [0.5, 0.8])
            time.sleep(self.wait_time)
            # 视频
            # poco("android.widget.LinearLayout").offspring("android:id/tabs").child("android.widget.RelativeLayout")[
            #     1].child("com.ss.android.article.lite:id/axy").click()
            # poco("android.widget.LinearLayout").offspring("android:id/tabs").child("android.widget.RelativeLayout")[
            #     1].child("com.ss.android.article.lite:id/axy").click()
            # time.sleep(self.wait_time)
            # poco.swipe([0.5, 0.2], [0.5, 0.8])
            # time.sleep(self.wait_time)
            # 评论
            # poco("com.ss.android.article.lite:id/ank").click()
            # time.sleep(self.wait_time)
            # 返回
            # poco("com.ss.android.article.lite:id/aid").click()

    def start1(self):
        pool = multiprocessing.Pool(processes=10)
        #usb
        pool.apply_async(self.vivo_usb)  # 维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去
        time.sleep(self.wait_time)
        pool.apply_async(self.huawei_usb)
        time.sleep(self.wait_time)
        pool.apply_async(self.xiaomi_usb)
        time.sleep(self.wait_time)
        pool.apply_async(self.oppo_usb)
        time.sleep(self.wait_time)
        #wifi
        # pool.apply_async(self.vivo_wifi)  # 维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去
        # pool.apply_async(self.huawei_wifi)
        # pool.apply_async(self.xiaomi_wifi)
        # pool.apply_async(self.oppo_wifi)
        pool.close()
        pool.join()  # 调用join之前，先调用close函数，否则会出错。执行完close后不会有新的进程加入到pool,join函数等待所有子进程结束

        #线程次
        # pool = ThreadPoolExecutor(max_workers=10)
        # pool.submit(self.vivo_usb)
        # pool.submit(self.huawei_usb)
        # pool.submit(self.xiaomi_usb)



if __name__ == "__main__":
    phone_wall = PhoneWall()
    phone_wall.start1()



