from scrapy.crawler import CrawlerProcess

from src.helper.scraper.ImdbSpider import ImdbSpider


def scraper():
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

        'DOWNLOAD_DELAY': 1,
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'IMDB.csv'
    }
    process = CrawlerProcess(settings)
    process.crawl(ImdbSpider)
    process.start()
    process.join()


if __name__ == "__main__":
    scraper()

