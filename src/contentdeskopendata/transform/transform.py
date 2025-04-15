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
                "name": product["values"]['name'],
                #"description": product["values"]["description"],
                "category": product["categories"],
                #"image": product["values"]["image"],
                #"url": product["values"]["url"]
            })
            
        return jsonLD
    
    def getTransformProducts(self):
        return self.transformProducts