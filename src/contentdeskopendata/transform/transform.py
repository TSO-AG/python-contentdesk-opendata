import json

class Transform:
    
    def __init__(self, extractProducts):
        self.extractProducts = extractProducts
        self.transformProducts = self.transformToJSONLD()
    
    def transformToJSONLD(self):
        jsonLD = []
        for product in self.extractProducts:
            jsonLD.append({
                "@context": "http://schema.org/",
                "@type": product["family"],
                "identifier	": product["identifier"],
                "name": self.languageToJSONLD(product["values"]['name']),
                #"description": product["values"]["description"],
                "category": product["categories"],
                #"image": product["values"]["image"],
                #"url": product["values"]["url"]
            })
            
        return jsonLD
    
    def getTransformProducts(self):
        return self.transformProducts
    
    def languageToJSONLD(self, languageValue):
        product = {}
        for language in languageValue:
            local = language['locale']
            product[local] = {}
            nameValue = language['data']
            product[local] = nameValue
            
        return product