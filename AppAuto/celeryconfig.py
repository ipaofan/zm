#!/usr/bin/env python
#-*- coding:utf-8 -*-

from kombu import Exchange,Queue

BROKER_URL = "redis://127.0.0.1:6379/1"
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/2"

CELERY_QUEUES = (
Queue("default",Exchange("default"),routing_key="default"),
Queue("for_task_A",Exchange("for_task_A"),routing_key="for_task_A"),
Queue("for_task_B",Exchange("for_task_B"),routing_key="for_task_B")
)
# 路由
CELERY_ROUTES = {
'tasks.taskA':{"queue":"for_task_A","routing_key":"for_task_A"},
'tasks.taskB':{"queue":"for_task_B","routing_key":"for_task_B"}
}

# 新增加的定时任务部分
CELERY_TIMEZONE = 'UTC'
CELERYBEAT_SCHEDULE = {
    'taskA_schedule' : {
        'task':'tasks.taskA',
        'schedule':60,
        'args':(5,6)
    },
    'taskB_scheduler' : {
        'task':"tasks.taskB",
        "schedule":10,
        "args":(10,20,30)
    },
    'add_schedule': {
        "task":"tasks.add",
        "schedule":5,
        "args":(1,2)
    }
}