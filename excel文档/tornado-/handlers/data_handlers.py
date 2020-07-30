import datetime
import json
from time import sleep

from tornado.websocket import WebSocketHandler
import pymysql
from .util import fetchall_to_dict
users = set()

class DataWebSocketHandler(WebSocketHandler):

    def open(self, *args, **kwargs):
        users.add(self)

    def on_message(self, message):
        pass

    def on_close(self):
        users.remove(self)

    def check_origin(self, origin):
        return True

def get_data():
    # 各个博文的数量
    connect = pymysql.connect(
        host="150.158.123.234",
        user="qiaofeng",
        password="1025",
        database="test",
        port=3306
    )
    cursor = connect.cursor()
    sql = """
        SELECT 
          * 
        FROM 
          emp 
    """
    cursor.execute(sql)
    res = fetchall_to_dict(cursor)
    connect.close()
    return res


def create_blog_data():
    while True:
        data = get_data()
        now = datetime.datetime.now().strftime("%H:%M:%S")
        result = {
            "now": now,
            "data": data
        }
        if len(users) > 0:
            for i in users:
                i.write_message(json.dumps(result))
        print(len(users))
        sleep(5)

