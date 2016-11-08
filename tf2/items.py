# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
 
# class BuyItem(Item):
    

# class SellItem(Item):

class BuySellItem(Item):
    orderType=Field()
    isTradable=Field()
    isCraftable=Field()
    listingPrice=Field()
    itemClass=Field()
    quality=Field()
    title=Field()
    dataQName=Field()
    dataListingOffersUrl=Field()
    dataPrice=Field()
    dataPaintName=Field()
    dataLevel=Field()
    dataPaintPrice=Field()
    dataId=Field()
    dataOrigin=Field()
    availableQty=Field()
    itemType=Field()

class ItemStats(Item):
    buyOrderCount=Field()
    sellOrderCount=Field()
    buyOrderList=Field()
    sellOrderList=Field()
    url=Field()
    totalQty=Field()
