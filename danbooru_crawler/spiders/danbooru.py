import scrapy
from .. import settings
from .. import items
from urllib import parse


class DanbooruSpider(scrapy.Spider):
    # custom_settings = {"DOWNLOAD_DELAY": 0.3, "RANDOMIZE_DOWNLOAD_DELAY": True}

    name = "danbooru"
    allowed_domains = ["donmai.us"]
    url = "https://danbooru.donmai.us"
    start_urls = [f"https://danbooru.donmai.us/posts?tags={settings.SEARCH_KEYS}"]

    def parse(self, response):
        """搜索页"""
        for _ in response.xpath('//a[@class="post-preview-link"]/@href').getall():
            pic_page_url = parse.urljoin(self.url, _)
            self.logger.info(f"图片详情页 {pic_page_url}")
            yield scrapy.Request(
                url=pic_page_url, callback=self.parse_pic_page_url, priority=2
            )
        # 下一页
        next_url = response.xpath('//a[@rel="next" and @href]/@href').get()
        if next_url is not None:
            next_url = parse.urljoin(self.url, next_url)
            self.logger.info(f"下一页 {next_url}")
            yield scrapy.Request(url=next_url, callback=self.parse, priority=3)

    def parse_pic_page_url(self, response):
        """图片详情页"""
        pic_page_url_list = response.xpath(
            '//div/article/div/a[@class="post-preview-link"]/@href'
        ).getall()
        if len(pic_page_url_list) > 1:
            pic_page_url_list = pic_page_url_list[1:]
        self.logger.info(f"图片资源页 {response.url}")
        yield self.parse_pic_url(response)
        for _ in pic_page_url_list:
            pic_page_url = parse.urljoin(self.url, _)
            self.logger.info(f"套图url {pic_page_url}")
            yield scrapy.Request(
                url=pic_page_url, callback=self.parse_pic_url, priority=1
            )

    def parse_pic_url(self, response):
        """推送"""
        pic_url = response.xpath("//section/picture/source/@srcset").get()
        self.logger.info(f"图片url {pic_url}")
        img_items = items.ImagedownloadItem()
        img_items["image_urls"] = [pic_url]
        return img_items
