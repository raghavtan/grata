"""

"""
from vibora.request import Request
from vibora.cache import CacheEngine


class DefaultCacheEngine(CacheEngine):
    """

    """

    async def get(self, request: Request):
        """

        :param request:
        :return:
        """
        return self.cache.get(request.url)

    async def store(self, request: Request, response):
        """

        :param request:
        :param response:
        :return:
        """
        self.cache[request.url] = response
