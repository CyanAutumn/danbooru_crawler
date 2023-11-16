import scrapy
from .. import settings
from .. import items
from urllib import parse


class DanbooruSpider(scrapy.Spider):
    # custom_settings = {"DOWNLOAD_DELAY": 0.3, "RANDOMIZE_DOWNLOAD_DELAY": True}

    name = "danbooru"
    allowed_domains = ["donmai.us"]
    url = "https://danbooru.donmai.us"
    start_urls = [f"https://danbooru.donmai.us/posts?tags={settings.SEARCH_TAG}"]

    def parse(self, response):
        """搜索页"""
        # 详情页
        for _ in response.xpath('//a[@class="post-preview-link"]/@href').getall():
            self.logger.info(f"详情页 {parse.urljoin(self.url, _)}")
            yield response.follow(_, callback=self.parse_pic_page_url, priority=1)
        # 下一页
        next_url = response.xpath('//a[@rel="next" and @href]/@href').get()
        if next_url is not None:
            self.logger.info(f"下一页 {parse.urljoin(self.url,next_url)}")
            yield response.follow(next_url, callback=self.parse, priority=2)

    def parse_pic_page_url(self, response):
        """详情页"""
        self.logger.info(f"详情页 {response.url}")
        img_url = None
        # 套图
        if settings.SEARCH_LINK:
            link_img_url_list = response.xpath(
                '//div/article[not(contains(@class,"current-post"))]/div/a/@href'
            ).getall()
            for _ in link_img_url_list:
                yield response.follow(_, callback=self.parse_pic_page_url, priority=1)

        # 抓取图片源地址
        if settings.SEARCH_TYPE == 0:
            img_url = response.xpath("//section/picture/source/@srcset").get()
        elif settings.SEARCH_TYPE == 1:
            img_url = response.xpath(
                '//li/a[@class="image-view-original-link"]/@href'
            ).get()
        if img_url is None:
            self.logger.info(f"空地址，可能是动图/视频")
        self.logger.info(f"资源url {img_url}")
        img_items = items.ImagedownloadItem()
        img_items["image_urls"] = [img_url]
        yield img_items
