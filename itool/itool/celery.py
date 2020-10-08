# 绝对路径导入
from __future__ import absolute_import
from celery import Celery
from django.conf import settings
import os

# 设置系统的环境配置用的是Django的
os.environ.setdefault('DJANGO_SETTING_MODULE', 'viodeClipping.settings')

# 实例化celery
app = Celery('mycelery')

app.conf.timezone = 'Asia/Shanghai'

# 指定celery的配置来源，用的是项目的配置文件settings.py
app.config_from_object('django.conf:settings')

# 让celery自动去发现的任务
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
