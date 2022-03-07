import json
from json import JSONEncoder


class ProductClass:
    def __init__(self, name, id, description, brand, link, lastUpdated, categories, tags, productOptions, images, attributes, variants):
        self.name = name
        self.id = id
        self.description = description
        self.brand = brand
        self.link = link
        self.lastUpdated = lastUpdated
        self.categories = categories
        self.tags = tags
        self.productOptions = productOptions
        self.images = images
        self.attributes = attributes
        self.variants = variants
        #self.collections = collections

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

# subclass JSONEncoder
class ProductEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__

class ProductOptionsClass:
    def __init__(self, name, position, values):
        self.name = name
        self.position = position
        self.values = values

class ImagesClass:
    def __init__(self, position, alt, scr, variantIds):
        self.scr = scr
        self.alt = alt
        self.position = position
        self.variantIds = variantIds

class ImagesClass:
    def __init__(self, position, alt, scr):
        self.scr = scr
        self.alt = alt
        self.position = position
        
        

class AttributeClass:
    def __init__(self, name,values):
        self.name = name
        self.values = values

class VariantClass:
    def __init__(self, name, id, prices, availableForPurchase, inventoryQuantity, productOptionValues, link, lastUpdated):
        self.name = name
        self.id = id
        self.prices = prices
        self.availableForPurchase = availableForPurchase
        self.inventoryQuantity = inventoryQuantity
        self.productOptionValues = productOptionValues
        self.link = link
        self.lastUpdated = lastUpdated
        #self.attributes = attributes

class ProductOptionValueClass:
    def __init__(self, name,values):
        self.name = name
        self.values = values

class PriceClass:
    def __init__(self, currencyCode, amount, activeTime, expirationTime, compareAtPrice):
        self.currencyCode = currencyCode
        self.amount = amount
        self.activeTime = activeTime
        self.expirationTime = expirationTime
        self.compareAtPrice = compareAtPrice

#Helper method to check value of field. Not needed when using .get()
#Must be aadded to main class to work
def catchKeyError(JsonRecord, elementName):
    try:
        value = JsonRecord[elementName]
    except KeyError:
        return 0
    else:
        return value


