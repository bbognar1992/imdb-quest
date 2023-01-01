from scrapy.crawler import CrawlerProcess

from src.helper.scraper.ImdbSpider import ImdbSpider


def scraper(output_path: str, test_mode: bool = False):
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
    if test_mode:
        settings['CLOSESPIDER_PAGECOUNT'] = 2

    process = CrawlerProcess(settings)
    process.crawl(ImdbSpider)
    process.start()
    process.join()