import logging

from scrapy.spiders import Spider

from .ImdbMovie import ImdbMovie
from .functions import value_converter, get_number_of_oscars, get_search_safely

modul_Logger = logging.getLogger('imdb_quest.scraper.helper.imdbspider')


class ImdbSpider(Spider):
    """Class for determine what and how to scrape in the IMDB website."""

    name = 'imdbspider'
    allowed_domains = ['imdb.com']
    start_urls = ['http://www.imdb.com/chart/top']
    limit = 0

    def parse(self, response, **kwargs):
        if ImdbSpider.limit == 0:
            for href in response.css("td.titleColumn a::attr(href)").getall():
                yield response.follow(url=href, callback=self.parse_movie)
        else:
            for i in range(1, ImdbSpider.limit + 1):
                try:
                    href = response.css(f"tr:nth-child({i}) > td.titleColumn a::attr(href)").get()
                    yield response.follow(url=href, callback=self.parse_movie)
                except Exception as err:
                    modul_Logger.debug(err)
                    break

    @staticmethod
    def parse_movie(response):
        """
        Saving values from the html page to an ImdbMovie object.

        :param response: Object contains the website html page.
        :return: ImdbMovie object.
        """
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

        modul_Logger.info(f"Scraped: {item['title']}")

        return item
