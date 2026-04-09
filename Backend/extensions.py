import logging
import pickle
import time

import redis
from celery import Celery
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger(__name__)


class InMemoryCache:
    """Fallback in-memory cache with TTL support."""

    def __init__(self):
        self.store = {}
        self.expiry = {}

    def get(self, key):
        if key in self.store:
            if time.time() < self.expiry.get(key):
                return self.store[key]
            del self.store[key]
            del self.expiry[key]
        return None

    def set(self, key, value, timeout=3600):
        self.store[key] = value
        self.expiry[key] = time.time() + timeout

    def delete(self, key):
        self.store.pop(key, None)
        self.expiry.pop(key, None)


class HybridCache:
    """Redis-first cache with an in-memory fallback."""

    def __init__(self):
        self.redis_client = None
        self.memory_cache = InMemoryCache()
        self.use_redis = False

    def init_app(self, app):
        """Initialize cache with Flask app config."""
        try:
            redis_url = app.config.get("REDIS_URL", "redis://localhost:6379/0")
            self.redis_client = redis.from_url(
                redis_url,
                decode_responses=False,
                socket_connect_timeout=2,
            )
            self.redis_client.ping()
            self.use_redis = True
            logger.info("Redis cache initialized: %s", redis_url)
        except (redis.ConnectionError, redis.TimeoutError) as exc:
            logger.warning("Redis unavailable, using in-memory cache: %s", exc)
            self.use_redis = False
        except Exception as exc:
            logger.warning("Cache initialization error, using in-memory cache: %s", exc)
            self.use_redis = False

    def get(self, key):
        try:
            if self.use_redis and self.redis_client:
                value = self.redis_client.get(key)
                return pickle.loads(value) if value else None
        except Exception as exc:
            logger.warning("Redis get failed, falling back to memory: %s", exc)
            self.use_redis = False
        return self.memory_cache.get(key)

    def set(self, key, value, timeout=3600):
        if self.use_redis and self.redis_client:
            try:
                self.redis_client.setex(key, timeout, pickle.dumps(value))
                return
            except Exception as exc:
                logger.warning("Redis set failed, using memory: %s", exc)
                self.use_redis = False
        self.memory_cache.set(key, value, timeout)

    def delete(self, key):
        if self.use_redis and self.redis_client:
            try:
                self.redis_client.delete(key)
                return
            except Exception as exc:
                logger.warning("Redis delete failed: %s", exc)
                self.use_redis = False
        self.memory_cache.delete(key)


db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
mail = Mail()
cache = HybridCache()
celery = Celery(__name__)
