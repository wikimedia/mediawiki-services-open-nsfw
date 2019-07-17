from aiohttp import web
from routes.root import Root
from routes.score import Score


class NSFWApp(web.Application):
    def __init__(self):
        super().__init__()
        self.router.add_route("get", "/v1/", Root)
        self.router.add_route("post", "/v1/score", Score)
