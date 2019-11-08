#!/usr/bin/env python
#-*- coding:utf-8 -*-
from celery import Celery

app = Celery()
app.config_from_object("celeryconfig")  # 指定配置文件
import multiprocessing
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from airtest.core.api import *
import time

loop_num = 1000


@app.task
def taskA(x,y):
    device_vivo = connect_device('android:339b19f1')  # vivo
    poco_vivo = AndroidUiautomationPoco(device=device_vivo, use_airtest_input=True, screenshot_each_action=False)
    device_huawei = connect_device('android:T7G0215804000411')
    poco_huawei = AndroidUiautomationPoco(device=device_huawei, use_airtest_input=True, screenshot_each_action=False)

    for i in range(1):
        #     poco1.swipe([0.5, 0.8], [0.5, 0.2])
        # 首页
        poco_vivo("android.widget.LinearLayout").offspring("android:id/tabs").child("android.widget.RelativeLayout")[
            0].child("com.ss.android.article.lite:id/axy").click()
        poco_vivo("android.widget.LinearLayout").offspring("android:id/tabs").child("android.widget.RelativeLayout")[
            0].child("com.ss.android.article.lite:id/axy").click()
        time.sleep(10)
        poco_vivo.swipe([0.5, 0.8], [0.5, 0.2])
        time.sleep(10)
        # 视频
        poco_vivo("android.widget.LinearLayout").offspring("android:id/tabs").child("android.widget.RelativeLayout")[
            1].child("com.ss.android.article.lite:id/axy").click()
        poco_vivo("android.widget.LinearLayout").offspring("android:id/tabs").child("android.widget.RelativeLayout")[
            1].child("com.ss.android.article.lite:id/axy").click()
        time.sleep(10)
        poco_vivo.swipe([0.5, 0.8], [0.5, 0.2])
        time.sleep(10)
        # 评论
        poco_vivo("com.ss.android.article.lite:id/ank").click()
        time.sleep(20)
        # 返回
        poco_vivo("com.ss.android.article.lite:id/aid").click()

            # 首页
        poco_huawei("android.widget.LinearLayout").offspring("android:id/tabs").child("android.widget.RelativeLayout")[
            0].child("com.ss.android.article.lite:id/axy").click()
        poco_huawei("android.widget.LinearLayout").offspring("android:id/tabs").child("android.widget.RelativeLayout")[
            0].child("com.ss.android.article.lite:id/axy").click()
        time.sleep(10)
        poco_huawei.swipe([0.5, 0.8], [0.5, 0.2])
        time.sleep(10)
        # 视频
        poco_huawei("android.widget.LinearLayout").offspring("android:id/tabs").child("android.widget.RelativeLayout")[
            1].child("com.ss.android.article.lite:id/axy").click()
        poco_huawei("android.widget.LinearLayout").offspring("android:id/tabs").child("android.widget.RelativeLayout")[
            1].child("com.ss.android.article.lite:id/axy").click()
        time.sleep(10)
        poco_huawei.swipe([0.5, 0.8], [0.5, 0.2])
        time.sleep(10)
        # 评论
        poco_huawei("com.ss.android.article.lite:id/ank").click()
        time.sleep(20)
        # 返回
        poco_huawei("com.ss.android.article.lite:id/aid").click()
    return x + y

@app.task
def taskB(x,y,z):
    return x + y + z

@app.task
def add(x,y):
    return x + y