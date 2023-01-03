import logging
import pathlib

from scrapy.crawler import CrawlerProcess

from src.helper.scraper.ImdbSpider import ImdbSpider

modul_Logger = logging.getLogger('imdb_quest.scraper')


def scraper(output_path: str, limit: int = 0) -> None:
    """
    Scraping the IMDB top 250 movie list and download the data to
    a file in CSV format.

    :param output_path: File path where the scraper should put the data.
    :param limit: Number to limit the parsed movies.
    :return: None
    """

    logging.getLogger('scrapy').propagate = False
    logging.getLogger('faker').propagate = False
    logging.getLogger('scrapy_fake_useragent').propagate = False
    logging.getLogger('filelock').propagate = False

    settings = {
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

        'DOWNLOAD_DELAY': 0.5,
        'LOG_LEVEL': 'WARNING',
        'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7',
        'FEEDS': {
            pathlib.Path(output_path): {
                'format': 'csv',
                'fields': ['title', 'imdb_rating', 'n_ratings', 'n_oscars']
            },
        }
    }

    if limit == 0:
        modul_Logger.info("No limit set for scraping")
    else:
        modul_Logger.info(f"The limit for scraping is {limit}.")

    modul_Logger.info("Started.")
    process = CrawlerProcess(settings)
    ImdbSpider.limit = limit
    process.crawl(ImdbSpider)
    process.start()  # the script will block here until the crawling is finished
