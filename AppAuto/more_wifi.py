from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from airtest.core.api import *
import time
from airtest.core.android import Android


def huawei():
    # device_1 = connect_device('android://192.168.103.156:48887/339b19f1?cap_method=javacap&touch_method=adb')
    # device_1 = connect_device('android:///192.168.103.156:48887?cap_method=javacap&touch_method=adb')
    # device_1 = connect_device('android:///192.168.0.108:48887?cap_method=javacap&touch_method=adb')
    device_1 = connect_device('android:///192.168.103.253:48887?cap_method=javacap&touch_method=adb')

    # device_1 = Android('android://192.168.103.156:48887?cap_method=javacap&touch_method=adb')
    poco = AndroidUiautomationPoco(device=device_1, use_airtest_input=True, screenshot_each_action=False)
    # poco(text="今日头条极速版").click()
    # poco(name="com.ss.android.article.lite:id/adg").click()
    # poco(name="com.ss.android.article.lite:id/qp").set_text("古剑奇谭三")
    for i in range(500):
        print(i)
        time.sleep(1)
        poco.swipe([0.5,0.8],[0.5,0.2])


def vivo():
    # device_1 = connect_device('android://192.168.103.156:48887/339b19f1?cap_method=javacap&touch_method=adb')
    # device_1 = connect_device('android:///192.168.103.156:48887?cap_method=javacap&touch_method=adb')
    device_1 = connect_device('android:///192.168.0.106:48887?cap_method=javacap&touch_method=adb')
    # device_1 = Android('android://192.168.103.156:48887?cap_method=javacap&touch_method=adb')
    poco = AndroidUiautomationPoco(device=device_1, use_airtest_input=True, screenshot_each_action=False)
    # poco(text="今日头条极速版").click()
    # poco(name="com.ss.android.article.lite:id/adg").click()
    # poco(name="com.ss.android.article.lite:id/qp").set_text("古剑奇谭三")
    for i in range(500):
        print(i)
        time.sleep(1)
        poco.swipe([0.5,0.8],[0.5,0.2])

if __name__ == '__main__':
    # vivo()
    huawei()