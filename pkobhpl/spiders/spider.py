import scrapy

from scrapy.loader import ItemLoader
from ..items import PkobhplItem
from itemloaders.processors import TakeFirst


class PkobhplSpider(scrapy.Spider):
	name = 'pkobhpl'
	start_urls = ['https://www.pkobh.pl/o-banku/aktualnosci/']

	def parse(self, response):
		post_links = response.xpath('//div[@class="news__item"]/a[1]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//ul[@class="pagination"]/li/a/@href').getall()
		yield from response.follow_all(next_page, self.parse)


	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="text"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="site-content__publish-date"]/text()').get()

		item = ItemLoader(item=PkobhplItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
