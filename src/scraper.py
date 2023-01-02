from scrapy.crawler import CrawlerProcess
from twisted.internet import reactor

from src.helper.scraper.ImdbSpider import ImdbSpider


def scraper(output_path: str, limit: int = 0):
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
        'FEED_FORMAT': 'csv',
        'FEED_URI': output_path
    }

    process = CrawlerProcess(settings)
    ImdbSpider.limit = limit
    process.crawl(ImdbSpider)
    d = process.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()  # the script will block here until all crawling jobs are finished
