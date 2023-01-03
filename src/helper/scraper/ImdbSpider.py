import logging

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
        movies = response.xpath('//*[@id="main"]/div/span/div/div/div[3]/table//tr')
        until = len(movies)
        if ImdbSpider.limit < len(movies):
            until = ImdbSpider.limit +1

        for movie in movies[1:until]:
            item = ImdbMovie()
            item['title'] = movie.css("td.titleColumn a::text").get()
            item['imdb_rating'] = movie.css("td.ratingColumn.imdbRating > strong::text").get()
            item['n_ratings'] = movie.css("td.ratingColumn.imdbRating > strong::attr(title)").get()

            href = movie.css("td.titleColumn a::attr(href)").get()
            yield response.follow(
                url=href,
                callback=self.pars_n_oscars,
                cb_kwargs=dict(item=item)
            )

    @staticmethod
    def pars_n_oscars(response, item):
        """
        Saving values from the html page to an ImdbMovie object.

        :param item:
        :param response: Object contains the website html page.
        :return: ImdbMovie object.
        """
        modul_Logger.info(f"Scraped: {item['title']}")
        item['n_oscars'] = response.xpath("//*[@id=\"__next\"]/main/div/section[1]/div/section/div/div[1]/section["
                                          "1]/div/ul/li/a[1]/text()").get(default="0")
        yield item
