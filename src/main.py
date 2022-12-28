from scrapy.crawler import CrawlerProcess

from src.helper.scraper.ImdbSpider import ImdbSpider


def scraper():
    process = CrawlerProcess()
    process.crawl(ImdbSpider)
    process.start()
    process.join()


if __name__ == "__main__":
    scraper()

