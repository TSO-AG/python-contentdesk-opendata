import json
import os
class Load:
    
    def __init__(self, transformProducts):
        self.transformProducts = transformProducts
        self.loadToFile("products")
    
    def loadToFile(self, fileName):
        if not os.path.exists("docs/api"):
            os.makedirs("docs/api")
        file = open("docs/api/"+fileName+".json", "w")
        file.write("[\n")
        for product in self.transformProducts:
            file.write(json.dumps(product, indent=4) + ",\n")
        file.write("]")
        file.close()
        
    def loadToDebug(self, fileName):
        if not os.path.exists("docs/debug"):
            os.makedirs("docs/debug")
        file = open("docs/debug/"+fileName+".json", "w")
        file.write("[\n")
        for product in self.transformProducts:
            file.write(json.dumps(product, indent=4) + ",\n")
        file.write("]")
        file.close()