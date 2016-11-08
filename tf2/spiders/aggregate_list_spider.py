

from scrapy import Spider
from scrapy.selector import Selector
from scrapy.http import Request

from tf2.items import BuySellItem,ItemStats

def ret0IfExist(arr):
    if len(arr):
        return str(arr[0].encode('UTF-8'));


class SpreadSheetSpider(Spider):
    name = "counter"
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
                    yield Request(url=newUrl,meta={'url':newUrl},callback=self.parseItemPage)


    def parseItemPage(self, response):
        itemStats=ItemStats()
        listing = Selector(response).xpath('//span/div/ul/li')
        listingIntent=listing.xpath('@data-listing_intent').extract()
        itemStats['buyOrderCount']=listingIntent.count("1")
        itemStats['sellOrderCount']=listingIntent.count("0")
        itemStats['url']=response.meta['url']
        itemStats['totalQty']=ret0IfExist(Selector(response).xpath('//*[@id="page-content"]/div[3]/div/ul/li[1]/strong[2]/text()').extract())
        itemStats['buyOrderList']=';'.join(Selector(response).xpath('//span/div/ul/li[@data-listing_intent = "1"]/@data-listing_price').extract())
        itemStats['sellOrderList']=';'.join(Selector(response).xpath('//span/div/ul/li[@data-listing_intent = "0"]/@data-listing_price').extract())
        yield itemStats    
