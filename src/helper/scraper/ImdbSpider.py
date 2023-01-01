import re
from scrapy.spiders import Spider

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


class ImdbSpider(Spider):
    name = 'imdbspider'
    allowed_domains = ['imdb.com']
    start_urls = ['http://www.imdb.com/chart/top']
    limit = 0

    def parse(self, response):
        if ImdbSpider.limit == 0:
            for href in response.css("td.titleColumn a::attr(href)").getall():
                yield response.follow(url=href, callback=self.parse_movie)
        else:
            for i in range(1, ImdbSpider.limit + 1):
                for href in response.css(f"tr:nth-child({i}) > td.titleColumn a::attr(href)").getall():
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
