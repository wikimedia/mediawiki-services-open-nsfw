from lib.metrics import SCORING_TIME
from prometheus_async.aio import time
from vendor.classify_nsfw import caffe_preprocess_and_compute, load_model
import numpy as np

nsfw_net, caffe_transformer = load_model()


@time(SCORING_TIME)
async def score(image: bytes) -> np.float64:
    return caffe_preprocess_and_compute(
        image,
        caffe_transformer=caffe_transformer,
        caffe_net=nsfw_net,
        output_layers=["prob"]
    )[1]
