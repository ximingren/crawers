from urllib.parse import urljoin

from scrapy.downloadermiddlewares.redirect import RedirectMiddleware, logger, BaseRedirectMiddleware
from scrapy.exceptions import IgnoreRequest, NotConfigured
from scrapy.mail import MailSender
from selenium import webdriver
from w3lib.url import safe_url_string


class CommonRedirectMiddleware(RedirectMiddleware):
    condition=True

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def _redirect(self, redirected, request, spider, reason):
        ttl = request.meta.setdefault('redirect_ttl', self.max_redirect_times)
        redirects = request.meta.get('redirect_times', 0) + 1

        if 'callback.58' in redirected.url:
            if self.condition:
                browser=webdriver.Chrome('/home/ximingren/Projects/Projects/crawer_summary/chromedriver')
                self.condition=False
                browser.get(redirected.url)
                return redirected
        if ttl and redirects <= self.max_redirect_times:
            redirected.meta['redirect_times'] = redirects
            redirected.meta['redirect_ttl'] = ttl - 1
            redirected.meta['redirect_urls'] = request.meta.get('redirect_urls', []) + \
                                               [request.url]
            redirected.dont_filter = request.dont_filter
            redirected.priority = request.priority + self.priority_adjust
            logger.debug("Redirecting (%(reason)s) to %(redirected)s from %(request)s",
                         {'reason': reason, 'redirected': redirected, 'request': request},
                         extra={'spider': spider})
            return redirected
        else:
            logger.debug("Discarding %(request)s: max redirections reached",
                         {'request': request}, extra={'spider': spider})
            raise IgnoreRequest("max redirections reached")

    def process_response(self, request, response, spider):
        if (request.meta.get('dont_redirect', False) or
                response.status in getattr(spider, 'handle_httpstatus_list', []) or
                response.status in request.meta.get('handle_httpstatus_list', []) or
                request.meta.get('handle_httpstatus_all', False)):
            self.condition=True
            return response

        allowed_status = (301, 302, 303, 307, 308)
        if 'Location' not in response.headers or response.status not in allowed_status:
            self.condition = True
            return response


        location = safe_url_string(response.headers['location'])

        redirected_url = urljoin(request.url, location)

        if response.status in (301, 307, 308) or request.method == 'HEAD':
            redirected = request.replace(url=redirected_url)
            return self._redirect(redirected, request, spider, response.status)

        redirected = self._redirect_request_using_get(request, redirected_url)
        return self._redirect(redirected, request, spider, response.status)


