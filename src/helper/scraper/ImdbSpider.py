import logging

from scrapy.http import HtmlResponse
from scrapy.spiders import Spider

from .ImdbMovie import ImdbMovie

modul_Logger = logging.getLogger('imdb_quest.scraper.helper.imdbspider')


class ImdbSpider(Spider):
    """Class for determine what and how to scrape in the IMDB website."""

    name = 'imdbspider'
    allowed_domains = ['imdb.com']
    start_urls = ['http://www.imdb.com/chart/top']
    limit = 0

    def parse(self, response, **kwargs):
        hrefs = response.css("td.titleColumn a::attr(href)").getall()
        until = len(hrefs)
        if ImdbSpider.limit < len(hrefs):
            until = ImdbSpider.limit
        for href in hrefs[0:until]:
            yield response.follow(url=href, callback=self.parse_movie)

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
        item['n_ratings'] = response.xpath("//*[@id=\"__next\"]/main/div/section[1]/section/div["
                                           "3]/section/section/div[3]/div[2]/div[1]/div[2]/div/div["
                                           "1]/a/div/div/div[ "
                                           "2]/div[3]/text()").get()
        item['n_oscars'] = response.xpath("//*[@id=\"__next\"]/main/div/section[1]/div/section/div/div[1]/section["
                                          "1]/div/ul/li/a[1]/text()").get(default="0")

        modul_Logger.info(f"Scraped: {item['title']}")

        return item
