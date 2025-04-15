import json
import os
from datetime import datetime

class Load:
    
    def __init__(self, transformProducts):
        self.transformProducts = transformProducts
        self.loadProducts = self.setLoadProducts()
        
    def getLoadProducts(self):
        return self.transformProducts
    
    def setLoadProducts(self):
        # All Products to api/products.json
        self.loadProductsToFile(self.getLoadProducts(), "products")
        
        # Create Main Type-Groupes
        # Place
        #   Accommodation
        #   CivicStructure
        #      AdministrativeArea
        #      TransportationSystem
        #   LocalBusiness
        #      FoodEstablishment
        #      LodgingBusiness
        #   Tour
        #   Webcam
        # Event
        # Product
        # CreativeWork
        #   MediaObject
        return self.transformProducts
    
    def loadProductsToFile(self, products, fileName):        
        # Check if folder exists
        if not os.path.exists("../api/"):
            os.makedirs("../api/")
        
        with open("../api/"+fileName+".json", "w") as file:
            file.write(json.dumps(products))