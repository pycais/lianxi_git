from handlers import chat_server
from handlers import index_handler
from handlers import data_handlers

urlpatterns = [
    (r"/login", chat_server.IndexHandler),
    (r"/chat", chat_server.ChatWebSocketHandler),
    (r"/index", index_handler.MyIndexHandler),
    (r"/user-count", index_handler.UserCountHandler),
    (r"/top-blog", index_handler.TopBlogHandler),
    (r"/visited-detail", index_handler.VisitedDetailHandler),
    (r"/ws/data", data_handlers.DataWebSocketHandler),
]