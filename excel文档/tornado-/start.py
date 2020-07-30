import asyncio
import threading

from tornado.options import define, options, parse_command_line
from tornado.web import Application
import tornado.ioloop
import config
import urls
from handlers import chat_server
from handlers import data_handlers
from tornado.platform.asyncio import AnyThreadEventLoopPolicy
define("port", default=12341, type=int)

if __name__ == '__main__':
    asyncio.set_event_loop_policy(AnyThreadEventLoopPolicy())
    threading.Thread(target=chat_server.listion_msg, daemon=True).start()
    threading.Thread(target=data_handlers.create_blog_data, daemon=True).start()

    app = Application(
        urls.urlpatterns, **config.settings
    )
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()