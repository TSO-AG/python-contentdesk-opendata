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
        # TODO: Fix Folder Path by Settings
        if not os.path.exists("../docs/api/"):
            os.makedirs("../docs/api/")
        
        with open("../docs/api/"+fileName+".json", "w") as file:
            file.write(json.dumps(products))
        
    def debugToFile(products, fileName):
         # get current date and time
        current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        #print("Current date & time : ", current_datetime)
        
        # convert datetime obj to string
        str_current_datetime = str(current_datetime)
        # Check if folder exists
        if not os.path.exists("../debug/"+str_current_datetime):
            os.makedirs("../debug/"+str_current_datetime+"/")
        
        with open("../debug/"+str_current_datetime+"/"+fileName+".json", "w") as file:
            file.write(json.dumps(products))