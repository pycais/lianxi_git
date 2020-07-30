import datetime

import random
import redis

from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler

class IndexHandler(RequestHandler):

    def get(self, *args, **kwargs):
        self.render("login.html")

    def post(self, *args, **kwargs):
        name = self.get_argument("name", "tom%d" % random.randint(1, 10000))
        self.set_secure_cookie("u_name", name)
        self.render("chat.html")

def listion_msg():
    client = redis.StrictRedis(db=11)

    pb = client.pubsub()
    pb.subscribe("1807", "1800")

    for i in pb.listen():
        if i.get("type") == "message":
            msg = i.get("data").decode()
            for i in ChatWebSocketHandler.users:
                i.write_message(msg)

class ChatWebSocketHandler(WebSocketHandler):
    users = set()
    def open(self, *args, **kwargs):
        print("链接上了")
        # 当有客户端链接过来的时候
        self.u_name = self.get_secure_cookie("u_name").decode()
        # 记录我们的登录用户是谁
        self.users.add(self)
        msg = "【%s】上线啦【%s】" % (self.u_name, datetime.datetime.now().strftime("%H:%M"))
        for i in self.users:
            if i is not self:
                i.write_message(msg)

    def on_message(self, message):

        msg = "【%s】:%s" % (self.get_secure_cookie("u_name").decode(), message)
        for i in self.users:
            i.write_message(msg)

    def on_close(self):
        self.users.remove(self)
        msg = "【%s】已经下线了" % (self.get_secure_cookie("u_name"))
        for i in self.users:
            i.write_message(msg)

    def check_origin(self, origin):
        return origin.endswith("sharemsg.cn:12341")