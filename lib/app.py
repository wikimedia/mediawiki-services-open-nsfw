from aiohttp import web
from prometheus_async import aio
from routes.root import Root
from routes.score import Score


class NSFWApp(web.Application):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.router.add_route("get", "/v1/", Root)
        self.router.add_route("post", "/v1/score", Score)
        self.router.add_get("/v1/metrics", aio.web.server_stats)
