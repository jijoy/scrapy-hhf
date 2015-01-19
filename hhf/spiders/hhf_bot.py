# -*- coding: utf-8 -*-
import scrapy
from hhf.items import HhfItem

class HhfBotSpider(scrapy.Spider):
    name = "hhf_bot"
    allowed_domains = ["heyheyfriends.com"]
    start_urls = (
        'http://www.heyheyfriends.com/newvideos.html?&page=20',
    )
    # self.show_chain = []
    def parse(self, response):
        self.show_chain = []
        selector = scrapy.Selector(response)
        for row in selector.xpath("//div[@id='newvideos_results']/table/tr")[1:]:
            tds = row.xpath('.//td')

            img_url = tds[0].xpath('.//a/img/@src').extract()[0]
            link = tds[0].xpath(".//a/@href").extract()[0]
            artist = tds[1].xpath("./text()").extract()[0]
            title = tds[2].xpath(".//a/text()").extract()[0]
            added = tds[3].xpath("./text()").extract()[0]
            # print img_url
            self.show_chain.append(scrapy.http.Request(
                link,callback=self.parse_episode,
                meta={'image_url':img_url,'artist':artist,'title':title,'added':added}))
        #Handle pagination
        pagination = selector.css('.pagination a')
        if 'next' in pagination[-1].xpath('.//text()').extract()[0]:
            link = pagination[-1].xpath('.//@href').extract()[0]
            link = 'http://www.heyheyfriends.com/'+link
            self.show_chain.append(scrapy.http.Request(link,callback=self.parse,errback = lambda x: self.download_errback(x, link)))

        if self.show_chain:
            yield self.show_chain.pop(0)


    def download_errback(self,response,link):
        print 'Error , but ignoring it.****************'
        if self.show_chain:
            yield self.show_chain.pop(0)

    def parse_episode(self,response):
        if response.status == 200 :
            print 'Response Meta = %s'%response.meta
            selector = scrapy.Selector(response)
            item = HhfItem()
            item['url']  = response.url
            item['image_url'] = response.meta['image_url']
            item['video_title'] = response.meta['title']
            item['artist'] = response.meta['artist']
            item['added_date'] = response.meta['added']
            category_string = selector.xpath("//div[@id='detail_page_vid_info']/a[2]/text()").extract()[0]
            item['category'] = category_string
            view_string = str(selector.xpath("//div[@id='detail_page_vid_info']/strong[3]/following-sibling::text()")[3].extract())
            print '||||***********%s'%view_string
            if ':' in view_string:
                item['views'] = view_string.split(':')[1].strip()
            else:
                view_string = str(selector.xpath("//div[@id='detail_page_vid_info']/strong[3]/following-sibling::text()")[4].extract())
                if ':' in view_string:
                    item['views'] = view_string.split(':')[1].strip()
            embeded_urls = selector.xpath(".//div[@id='Playerholder']/embed/@src").extract()
            if len(embeded_urls) > 0 :
                item['embed_url'] = embeded_urls
            else :
                embeded_urls = selector.xpath(".//div[@id='Playerholder']/iframe/@src").extract()
                if len(embeded_urls) > 0:
                    item['embed_url'] = embeded_urls
                else:
                    embeded_urls = selector.xpath(".//div[@id='Playerholder']/object/embed/@src").extract()
                    if len(embeded_urls) > 0:
                        item['embed_url'] = embeded_urls
                    else :
                        embeded_urls= selector.xpath("//div[@id='detail_page']/div[2]/a/@href").extract()
                        item['embed_url'] = embeded_urls
            yield item
        if self.show_chain:
            yield self.show_chain.pop(0)
