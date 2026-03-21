import redis
import json
import os
from functools import lru_cache
from config import get_config

cfg = get_config()

redis_client = redis.from_url(cfg.CELERY_BROKER_URL, decode_responses=True)

def get_cache(key: str):
    try:
        return json.loads(redis_client.get(key) or '{}')
    except:
        return {}

def set_cache(key: str, value: dict, ttl: int = 3600):
    redis_client.setex(key, ttl, json.dumps(value))

def cache_job_result(job_id: str, result: dict):
    set_cache(f'job:{job_id}', result, 86400)  # 24h

def get_cached_job(job_id: str):
    return get_cache(f'job:{job_id}')

