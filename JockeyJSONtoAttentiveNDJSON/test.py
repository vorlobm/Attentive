import json
from testing.attentiveClass import ProductClass, PriceClass, ProductOptionValueClass, ProductOptionsClass, VariantClass, ImagesClass, ProductEncoder


def attentiveJSONConverter (filePath):
    # Opening Jockey JSON file
    # returns JSON object as a dictionary
    # r = filename of Jockey File
    with open(filePath, "r") as r:
        data = json.load(r)


    # Loop through each Item
    for item in data['ItemCollection']['Item']:
        url = item['@productUrl']
        
        #grab only values of cateogory records
        categories = []
        for currentcategory in item['ns1:ClassificationCollection']['ns1:ClassificationData']:
            #check if already exsists or if its none
            value = str(currentcategory.get('@value'))
            if (value not in categories) and (value is not None):
                categories.append(value) 

        #grab entire tag array in one call since tags are not declared as individual records
        tags = item['ns1:DescriptionCollection']['ns1:TagCollection'].get('ns1:Tag')
        
        #loop through top level of images
        images = []
        imgCount = 0
        for currentimage in item['ns1:ImageCollection']['ns1:ImageData']:
                image = ImagesClass(imgCount, currentimage.get('@name'), currentimage.get('@value'))
                imgCount = imgCount + 1
                images.append(image)


        #loop through each Item Variant
        variants = []
        colors = []
        sizes = []
        
        for variant in item['ns1:VariationCollection']['ns1:VariationData']:
            productOptionValues = []
            productOptionValues.append(ProductOptionValueClass("color", variant.get('@color')))
            productOptionValues.append(ProductOptionValueClass("size", variant.get('@size')))

            #add any distinct sizes and colors to lists
            if variant.get('@color') not in colors:
                colors.append(variant.get('@color'))
            if variant.get('@size') not in sizes:
                sizes.append(variant.get('@size'))
            
            
            #can probably gid rid of this
            prices = []
            listprice = 0
            saleprice = 0
            for currentprice in variant['ns1:PriceCollection']['ns1:PriceData']:
                if currentprice.get('@priceType') is "ListPrice":
                    listprice = currentprice.get('@priceValue')
                elif currentprice.get('@priceType') is "SalePrice":
                    saleprice = currentprice.get('@priceValue')
                else:
                    continue
                if saleprice > 0:
                    price = PriceClass("USD",saleprice,currentprice.get('@priceStartDate'),currentprice.get('@priceEndDate') , listprice)
                else:
                    price = PriceClass("USD",listprice,currentprice.get('@priceStartDate'),currentprice.get('@priceEndDate') , "")
                prices.append(price)

            #loop through each image for each variant and add it to total images for this item
            for currentimage in variant['ns1:ImageCollection']['ns1:ImageData']:
                image = ImagesClass(imgCount, currentimage.get('@name'), currentimage.get('@value'))
                imgCount = imgCount + 1
                images.append(image)

            variant = VariantClass(variant.get('@variationName'), variant.get('@itemId'), prices, bool(variant['ns1:Inventory'].get('@status')), variant['ns1:Inventory'].get('@onHandQuantity'), productOptionValues, url, variant.get('@lastModifiedDate'))
            variants.append(variant)
        
        #create product options array and ProductOptions Objects using color and size
        productOptions = []
        productOptions.append(ProductOptionsClass("color", 0, colors))
        productOptions.append(ProductOptionsClass("size", 1, sizes))
        
        #create product object
        product = ProductClass(item['@name'], item['@itemId'],item['ns1:DescriptionCollection']['ns1:DescriptionData']['@description'], item['ns1:DescriptionCollection']['ns1:DescriptionData']['@brand'], url, item['@lastModifiedDate'], categories, tags, productOptions, images, "", variants)
        
        #turn product object to dictionary with 4 space indent then encode it to JSON
        productJSONData = json.dumps(product, indent=4, cls=ProductEncoder)
        print(productJSONData)
    
    # Create new file 
    #writes productJSON object to file
    # w = filename of new file
    with open("newFile.json", 'w') as w:
        w.write(productJSONData)

