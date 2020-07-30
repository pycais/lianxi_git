from tornado.web import RequestHandler

class MyIndexHandler(RequestHandler):

    def get(self, *args, **kwargs):
        self.render("index/index.html", template_id=1)


class UserCountHandler(RequestHandler):

    def get(self, *args, **kwargs):
        self.render("index/index.html", template_id=2)


class TopBlogHandler(RequestHandler):

    async def get(self, *args, **kwargs):
        await self.render("index/index.html", template_id=3)


class VisitedDetailHandler(RequestHandler):

    async def get(self, *args, **kwargs):
        await self.render("index/index.html", template_id=4)