import json
class Transform:
    def createJSONLD(self):
        jsonLD = []
        for product in self.produccts:
            jsonLD.append({
                "@context": "http://schema.org/",
                "@type": product["family"],
                "identifier	": product["identifier"],
                "name": product["values"]['name'],
                "description": product["values"]["description"],
                "category": product["categories"],
                "image": product["values"]["image"],
                "url": product["values"]["url"]
            })
            
        # create json
        
            
        return json.dump(jsonLD)