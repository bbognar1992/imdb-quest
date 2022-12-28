import re

import scrapy

from .ImdbMovie import ImdbMovie


def get_search_safely(response, xpath: str, default_return: str) -> str:
    try:
        return response.xpath(xpath).get()
    except Exception:
        return default_return


def get_number_of_oscars(raw_str: str) -> str:
    try:
        found = re.search(r"Won [\d]+ Oscar", raw_str)
        return found.group(0).replace("Won ", "").replace(" Oscar", "")
    except Exception:
        return "0"


def value_converter(x: str) -> str:
    if 'K' in x:
        if len(x) > 1:
            return str(int(float(x.replace('K', '')) * 1000))
        return str(1000)
    if 'M' in x:
        if len(x) > 1:
            return str(int(float(x.replace('M', '')) * 1000000))
        return str(1000000)
    if 'B' in x:
        return str(int(float(x.replace('B', '')) * 1000000000))
    return str(0)


class ImdbSpider(scrapy.Spider):
    name = 'imdbspider'
    allowed_domains = ['imdb.com']
    start_urls = ['http://www.imdb.com/chart/top']

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,
            "scrapy.downloadermiddlewares.retry.RetryMiddleware": None,
            "scrapy_fake_useragent.middleware.RandomUserAgentMiddleware": 400,
            "scrapy_fake_useragent.middleware.RetryUserAgentMiddleware": 401,
        },
        'FAKEUSERAGENT_PROVIDERS': [
            "scrapy_fake_useragent.providers.FakerProvider",
            "scrapy_fake_useragent.providers.FakeUserAgentProvider",
            "scrapy_fake_useragent.providers.FixedUserAgentProvider",
        ],

        'DOWNLOAD_DELAY': 2,
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'IMDB.csv'
    }

    def parse(self, response):
        """ This function parses a imdb movies response. Some contracts are mingled
        with this docstring.

        @url https://www.imdb.com/title/tt0268978/?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=1a264172-ae11-42e4-8ef7-7fed1973bb8f&pf_rd_r=3RNA5HNP3QXPZ21890XF&pf_rd_s=center-1&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_tt_142
        @returns 'A Beautiful Mind' 8.2 933000 4
        @scrapes title rating n_ratings n_oscars
        """
        for href in response.css("td.titleColumn a::attr(href)").getall():
            yield response.follow(url=href, callback=self.parse_movie)

    def parse_movie(self, response):
        item = ImdbMovie()
        item['title'] = response.xpath("//*[@id=\"__next\"]/main/div/section[1]/section/div[3]/section/section/div["
                                       "2]/div[1]/h1/text()").get()
        item['rating'] = response.xpath("//*[@id=\"__next\"]/main/div/section[1]/section/div[3]/section/section/div["
                                        "3]/div[2]/div[1]/div[2]/div/div[1]/a/div/div/div[2]/div[1]/span[1]/text("
                                        ")").get()
        item['n_ratings'] = value_converter(response.xpath("//*[@id=\"__next\"]/main/div/section[1]/section/div["
                                                           "3]/section/section/div[3]/div[2]/div[1]/div[2]/div/div["
                                                           "1]/a/div/div/div[ "
                                                           "2]/div[3]/text()").get())
        item['n_oscars'] = get_number_of_oscars(get_search_safely(response, "//*[@id=\"__next\"]/main/div/section["
                                                                            "1]/div/section/div/div[1]/section["
                                                                            "1]/div/ul/li/a[1]/text()", "0"))
        return item
