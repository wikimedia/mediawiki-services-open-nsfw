from aiohttp import web
import logging
from PIL import ImageFile
from lib.app import NSFWApp

# TODO: Get log level from service config
logging.basicConfig(level='INFO')

ImageFile.LOAD_TRUNCATED_IMAGES = True

web.run_app(NSFWApp())
