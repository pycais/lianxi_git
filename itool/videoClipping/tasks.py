from celery import task
import time


@task
def hello(loop):
    for i in range(loop):
        print(i)
        time.sleep(1)
    return loop * 2
