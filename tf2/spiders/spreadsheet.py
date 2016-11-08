
from scrapy import Spider
from scrapy.selector import Selector
from scrapy.http import Request

from tf2.items import BuySellItem

def ret0IfExist(arr):
    if len(arr):
        return str(arr[0].encode('UTF-8'));


class SpreadSheetSpider(Spider):
    name = "spreadsheet"
    allowed_domains = ["backpack.tf"]
    start_urls = [
        "http://backpack.tf/spreadsheet",
    ]
    def parse(self, response):
        types=['Unique','Genuine','Vintage','Unique','Strange','Haunted',"Collector's"]
        rows = Selector(response).xpath('//*[@id="pricelist"]/tbody/tr')
        for row in rows:
            item = BuySellItem()
            #sampleUrl http://backpack.tf/stats/Unique/A%20Color%20Similar%20to%20Slate/Tradable/Non-Craftable
            item['title']=ret0IfExist(row.xpath('td[1]/text()').extract())
            item['itemType']=ret0IfExist(row.xpath('td[2]/text()').extract())
            nonCraftable=ret0IfExist(row.xpath('td[1]/span/text()').extract())

            for type in types:
                newUrl='http://backpack.tf/stats/'
                newUrl+=type+'/'+item['title']+'/Tradable/'
                if nonCraftable:
                    newUrl+='Non-Craftable'
                else:
                    newUrl+='Craftable'
                    print(newUrl)
                    yield Request(url=newUrl,meta={'item':item},callback=self.parseItemPage)


    def parseItemPage(self, response):
        listing = Selector(response).xpath('//span/div/ul/li')
        item=response.meta['item']
        for lister in listing:
            item['availableQty']=ret0IfExist(lister.xpath('@data-listing_intent').extract())
            item['orderType']=ret0IfExist(lister.xpath('@data-listing_intent').extract())
            #item['title']=ret0IfExist(lister.xpath('@data-market_name').extract())
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

            yield item
