from aiohttp import web
import yaml


class Root(web.View):
    async def get(self):
        request = self.request
        if 'spec' in request.rel_url.query:
            with open('spec.yaml', 'r') as stream:
                return web.json_response(yaml.safe_load(stream))
        else:
            return web.Response(text='OK')
