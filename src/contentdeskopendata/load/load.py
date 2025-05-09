import json
import os
from datetime import datetime

class Load:
    
    def __init__(self, transformProducts, projectPath):
        self.projectPath = projectPath
        self.transformProducts = transformProducts
        self.typesClass = self.loadAllTypes()
        self.loadProducts = self.setLoadProducts()
        self.createMarkDownFile()
               
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
        
        self.createProductListbyParentTyp("Place")
        self.createProductListbyParentTyp("Accommodation")
        self.createProductListbyParentTyp("CivicStructure")
        self.createProductListbyParentTyp("AdministrativeArea")
        self.createProductListbyParentTyp("TransportationSystem")
        self.createProductListbyParentTyp("LocalBusiness")
        self.createProductListbyParentTyp("FoodEstablishment")
        self.createProductListbyParentTyp("LodgingBusiness")
        self.createProductListbyParentTyp("Tour")
        self.createProductListbyParentTyp("Webcam")
        self.createProductListbyParentTyp("Event")
        self.createProductListbyParentTyp("Product")
        self.createProductListbyParentTyp("CreativeWork")
        self.createProductListbyParentTyp("MediaObject")
        
        return self.transformProducts
    
    def createProductListbyParentTyp(self, typeClass):
        types = self.setTypesListbyParent(typeClass)
        products = self.getProductsbyTypes(types)
        self.loadProductsToFile(products, typeClass)
        return products
    
    def loadProductsToFile(self, products, fileName):        
        # Check if folder exists
        # TODO: Fix Folder Path by Settings
        print("Folder Path: ", self.projectPath+"/api/"+fileName+".json")
        if not os.path.exists(self.projectPath+"/api/"):
            os.makedirs(self.projectPath+"/api/")
        
        with open(self.projectPath+"/api/"+fileName+".json", "w") as file:
            file.write(json.dumps(products))
            
    def setTypesListbyParent(self, parentType):
        types = []
        for typeClass in self.typesClass:
            if self.typesClass[typeClass]['parent'] == parentType:
                types.append(typeClass)
            elif typeClass == parentType:
                types.append(typeClass)
        return types
    
    def getProductsbyTypes(self, types):
        products = []
        for product in self.transformProducts:
            if product.get("@type") in types:
                products.append(product)
                
        return products
    
    def loadAllTypes(self):
        types_file_path = os.path.join(self.projectPath, "types.json")
        print("Types File Path: ", types_file_path)
        if os.path.exists(types_file_path):
            with open(types_file_path, "r") as file:
                types = json.load(file)
            return types
        else:
            print(f"File {types_file_path} does not exist.")
            return []
        
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
            
    def createMarkDownFile(self):
        # create a markdown file with the name "data.md" in the projectPath
        markdown_file_path = os.path.join(self.projectPath, "data.md")
        with open(markdown_file_path, "w") as file:
            file.write("# Data Overview\n\n")
            file.write("This markdown file provides an overview of the data processed by the Load class.\n\n")
            file.write("## Product Types\n")
            for typeClass in self.typesClass:
                file.write(f"- {typeClass}\n")
                file.write("\n## Total Products\n")
                file.write(f"- {len(self.transformProducts)} products\n")
        print(f"Markdown file created at: {markdown_file_path}")