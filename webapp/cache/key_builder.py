from conf.config import settings


def get_user_cache_key(user_id: int) -> str:
    return f'{settings.REDIS_SIRIUS_CACHE_PREFIX}:user:{user_id}'
