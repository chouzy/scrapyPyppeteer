# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from pyppeteer import launch
from scrapy.http import HtmlResponse
import asyncio
from twisted.internet.defer import Deferred

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


def as_deferred(f):
    return Deferred.fromFuture(asyncio.ensure_future(f))


class PyppeteerMiddleware(object):
    async def _process_request(self, request, spider):
        """
        Process request and return a response
        :param request:
        :param spider:
        :return:
        """
        browser = await launch({'headless': False})
        page = await browser.newPage()
        py_response = await page.goto(request.url)
        await asyncio.sleep(5)
        html = await page.content()
        py_response.headers.pop('content-encoding', None)
        py_response.headers.pop('Content-Encoding', None)
        response = HtmlResponse(url=page.url, status=py_response.status, body=str.encode(html),
                                headers=py_response.headers, encoding='utf-8', request=request)
        await page.close()
        await browser.close()
        return response

    def process_request(self, request, spider):
        return as_deferred(self._process_request(request, spider))
