import yaml
import logging
import asyncio
import aiohttp
import async_timeout
import numpy as np
import uvloop
from aiohttp import web
from aiohttp.web import HTTPBadRequest, HTTPNotFound, HTTPUnsupportedMediaType

from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

from classify_nsfw import caffe_preprocess_and_compute, load_model
nsfw_net, caffe_transformer = load_model()

logger = logging.getLogger(__name__)


async def score(image: bytes) -> np.float64:
    return caffe_preprocess_and_compute(
        image,
        caffe_transformer=caffe_transformer,
        caffe_net=nsfw_net,
        output_layers=["prob"]
    )[1]

async def fetch(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            if response.status == 404:
                raise HTTPNotFound()
            return await response.read()

class Root(web.View):
    async def get(self):
        request = self.request
        if 'spec' in request.rel_url.query:
            with open('spec.yaml', 'r') as stream:
                return web.json_response(yaml.safe_load(stream))
        else:
            return web.Response(text='OK')

class Score(web.View):
    async def post(self):
        request = self.request
        data = await request.post()
        try:
            image = await fetch(session, data["url"])
            nsfw_prob = await score(image)
            return web.Response(text=nsfw_prob.astype(str))
        except KeyError:
            return HTTPBadRequest(text="Missing `url` POST parameter")
        except OSError as e:
            if "cannot identify" in str(e):
                raise HTTPUnsupportedMediaType(text="Invalid image")
            else:
                raise e


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
session = aiohttp.ClientSession()
app = web.Application()
app.router.add_route("get", "/v1/", Root)
app.router.add_route("post", "/v1/score", Score)
web.run_app(app)
