#buy div xpath "//*[@id="page-content"]/div[3]/div/div[3]/div/div[2]"
#sell div xpath "//*[@id="page-content"]/div[3]/div/div[3]/div/div[1]"

#buy values xpath "//*[@id="page-content"]/div[3]/div/div[3]/div/div[1]//span/div/ul/li/span[1]/text()"
#sell values xpath "//*[@id="page-content"]/div[3]/div/div[3]/div/div[2]//span/div/ul/li/span[1]/text()"

#total available inventory of this item "//*[@id="page-content"]/div[3]/div/ul/li[1]/strong[2]/text()"

#buy request paragraph text "//*[@id="page-content"]/div[3]/div/div[3]/div/div[2]//div/div[2]/p/text()"

#sell request paragraph text "//*[@id="page-content"]/div[3]/div/div[3]/div/div[1]//div/div[2]/p/text()"

#this is most useful
#get all the details from this li tag's attribute
#all details of sell order "//*[@id="page-content"]/div[3]/div/div[3]/div/div[1]//span/div/ul/li/"

#get all the details from this li tag's attribute
#all details of buy order "//*[@id="page-content"]/div[3]/div/div[3]/div/div[2]//span/div/ul/li"

#to get attributes use
#"//*[@id="page-content"]/div[3]/div/div[3]/div/div[2]//span/div/ul/li/@data-paint_price"

#every listing in single place
# xpath "$x('//span/div/ul/li')"
# /@data-listing_intent gives buys or sells
# /@data-listing_intent=1 --> sells
# /@data-listing_intent=0 --< buy

from scrapy import Spider
from scrapy.selector import Selector

from tf2.items import BuySellItem

def ret0IfExist(arr):
    if len(arr):
        return str(arr[0]);


class BuySellSpider(Spider):
    name = "tf2"
    allowed_domains = ["backpack.tf"]
    start_urls = [
        "https://backpack.tf/stats/Strange/A%20Hat%20to%20Kill%20For/Tradable/Craftable",
    ]
    def parse(self, response):
        listing = Selector(response).xpath('//span/div/ul/li')
        

        print(listing,'****************')
        for lister in listing:
            item = BuySellItem()
            item['orderType']=ret0IfExist(lister.xpath('@data-listing_intent').extract())
            item['title']=ret0IfExist(lister.xpath('@data-market_name').extract())
            item['isTradable'] =ret0IfExist(lister.xpath('@data-tradable').extract())
            item['isCraftable']=ret0IfExist(lister.xpath('@data-craftable').extract())
            item['listingPrice']=ret0IfExist(lister.xpath('@data-listing_price').extract())
            item['itemClass'] =ret0IfExist(lister.xpath('@data-class').extract())
            item['quality']=ret0IfExist(lister.xpath('@data-quality').extract())
            item['dataQName']=ret0IfExist(lister.xpath('@data-q_name').extract())
            item['dataListingOffersUrl']=ret0IfExist(lister.xpath('@data-listing_offers_url').extract())
            item['dataPrice']=ret0IfExist(lister.xpath('@data-price').extract())
            item['dataPaintName']=ret0IfExist(lister.xpath('@data-pain_name').extract())
            item['dataLevel'] =ret0IfExist(lister.xpath('@data-level').extract())
            item['dataPaintPrice'] =ret0IfExist(lister.xpath('@data-paint_price').extract())
            item['dataId'] =ret0IfExist(lister.xpath('@data-id').extract())
            item['dataOrigin'] =ret0IfExist(lister.xpath('@data-origin').extract())
            item['availableQty']=ret0IfExist(lister.xpath('//*[@id="page-content"]/div[3]/div/ul/li[1]/strong[2]/text()').extract())
            yield item
        # for question in questions:
        #     item = BuySellItem()
        #     item['title'] = question.xpath(
        #         'a[@class="question-hyperlink"]/text()').extract()[0]
        #     item['url'] = question.xpath(
        #         'a[@class="question-hyperlink"]/@href').extract()[0]
        #     yield item
