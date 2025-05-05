import json
import os
from datetime import datetime

class Load:
    
    def __init__(self, transformProducts, path):
        self.path = path
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
        projetctPath = os.path.dirname(os.path.abspath(__file__))
        print("Folder Path: ", projetctPath+"/"+self.path+"/api/")
        if not os.path.exists(projetctPath+"/"+self.path+"/api/"):
            os.makedirs(projetctPath+"/"+self.path+"/api/")
        
        with open(projetctPath+"/"+self.path+"/api/"+fileName+".json", "w") as file:
            file.write(json.dumps(products))
        
    def debugToFile(products, fileName, path):
         # get current date and time
        current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        #print("Current date & time : ", current_datetime)
        
        # convert datetime obj to string
        str_current_datetime = str(current_datetime)
        projetctPath = os.path.dirname(os.path.abspath(__file__))
        # Check if folder exists
        print("Folder Path: ", projetctPath+"/"+path+"/debug/"+str_current_datetime)
        if not os.path.exists(projetctPath+"/"+path+"/debug/"+str_current_datetime):
            os.makedirs(projetctPath+"/"+path+"/debug/"+str_current_datetime+"/")
        
        with open(projetctPath+"/"+path+"/debug/"+str_current_datetime+"/"+fileName+".json", "w") as file:
            file.write(json.dumps(products))