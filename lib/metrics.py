from prometheus_client import Summary

REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
SCORING_TIME = Summary('image_scoring_processing_seconds', 'Time spent scoring the fetched image')
