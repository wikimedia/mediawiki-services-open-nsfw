from aiohttp import ClientSession, web
from aiohttp.web import HTTPBadRequest, HTTPUnsupportedMediaType
import asyncio
import logging
from lib.scoring import score
from lib.util import fetch
import uvloop

logger = logging.getLogger('nsfwoid/score')

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
session = ClientSession()


class Score(web.View):
    async def post(self):
        request = self.request
        data = await request.post()
        try:
            url = data["url"]
            logger.info("Processing score request for URL: {0}".format(url))
            image = await fetch(session, url)
            nsfw_prob = await score(image)
            return web.Response(text=nsfw_prob.astype(str))
        except KeyError:
            raise HTTPBadRequest(text="Missing `url` POST parameter")
        except OSError as e:
            if "cannot identify" in str(e):
                raise HTTPUnsupportedMediaType(text="Invalid image")
            else:
                raise e
