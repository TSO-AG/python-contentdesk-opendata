import json
import os
from datetime import datetime

class Load:
    
    def __init__(self, transformProducts, projectPath):
        self.projectPath = projectPath
        self.transformProducts = transformProducts
        self.loadProducts = self.setLoadProducts()
               
    def getLoadProducts(self):
        return self.transformProducts
    
    def setLoadProducts(self):
        # All Products to api/products.json
        self.loadProductsToFile(self.transformProducts, "products")
        
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
        typesObjects = self.setLoadProductsByType(self.transformProducts, ["LocalBusiness", "FoodEstablishment", "LodgingBusiness"])
        self.loadProductsToFile(typesObjects, "LocalBusiness")
        
        return self.transformProducts
    
    def loadProductsToFile(self, products, fileName):        
        # Check if folder exists
        # TODO: Fix Folder Path by Settings
        print("Folder Path: ", self.projectPath+"api/")
        if not os.path.exists(self.projectPath+"api/"):
            os.makedirs(self.projectPath+"api/")
        
        with open(self.projectPath+"api/"+fileName+".json", "w") as file:
            file.write(json.dumps(products))
            
    def setLoadProductsByType(self, products, types):
        loadProducts = []
        for product in products:
            if product["@type"] in types:
                loadProducts.append(product)
                
        return loadProducts
        
    def debugToFile(products, fileName, projectPath):
         # get current date and time
        current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        #print("Current date & time : ", current_datetime)
        
        # convert datetime obj to string
        str_current_datetime = str(current_datetime)
        # Check if folder exists
        print("Folder Path: ", projectPath+"/debug/"+str_current_datetime)
        if not os.path.exists(projectPath+"/debug/"+str_current_datetime):
            os.makedirs(projectPath+"/debug/"+str_current_datetime+"/")
        
        with open(projectPath+"/debug/"+str_current_datetime+"/"+fileName+".json", "w") as file:
            file.write(json.dumps(products))