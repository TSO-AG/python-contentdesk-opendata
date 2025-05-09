import json
import os
from datetime import datetime

class Load:
    
    def __init__(self, transformProducts, projectPath, organization, name, website, organization_website, region):
        self.projectPath = projectPath
        self.organization = organization
        self.name = name
        self.website = website
        self.organization_website = organization_website
        self.region = region
        self.transformProducts = transformProducts
        self.countProducts = len(self.transformProducts)
        self.typesClass = self.loadAllTypes()
        self.loadProducts = self.setLoadProducts()
        self.createMarkDownFileIndex()
        self.createMarkDownFileDocumentation()
               
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
    
    def createMarkDownString(self, name, filename):
        string = ""
        
        string += "["+name+"](/api/"+filename+".json)\n"
        
        return string
    
    def checkLengthinFile(self, fileName):
        # load the JSON file to check the Objekt lenght in de File
        file_path = os.path.join(self.projectPath, "api", fileName + ".json")
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                data = json.load(file)
                # Check the length of the JSON object
                if isinstance(data, list):
                    length = len(data)
                    print(f"Length of {fileName}: {length}")
                    return length
                else:
                    print(f"{fileName} is not a list.")
                    return 0
    
    def createMarkDownFileIndex(self):
        # create a markdown file with the name "data.md" in the projectPath
        markdown_file_path = os.path.join(self.projectPath, "index.md")
        with open(markdown_file_path, "w", encoding='utf-8') as file:
            file.write("---\n")
            file.write("hide:\n")
            file.write("  - navigation\n")
            file.write("  - toc\n")
            file.write("---\n")
            file.write("# Willkommen auf dem OpenData Portal der "+self.organization+"\n\n")
            file.write(str(self.countProducts)+ " freie Datensätze\n\n")
            file.write("Hier finden Sie öffentlich zugängliche Datensätze aus der "+self.region+" wie Unterkünfte, Erlebnisse und Gastronomie. Die hier veröffentlichten Daten stehen kostenlos zur Verfügung und können mit einer [CC BY-SA](https://creativecommons.org/licenses/by-sa/4.0/deed.de) Lizenz frei wiederverwendet werden.\n\n")
            file.write("**Die Daten dürfen**\n\n")
            file.write("- vervielfältigt, verbreitet und weiter zugänglich gemacht werden\n- angereichert und bearbeitet werden\n- kommerziell genutzt werden\n\n")
            file.write("**Haftungsausschluss**\n\n")
            file.write("- Die "+self.organization+" schliesst jede Haftung für direkte und indirekte Schäden durch die Datennutzung aus. Sie übernimmt keine Garantie für die Aktualität, Richtigkeit, Vollständigkeit und Genauigkeit der veröffentlichten Daten.\n\n")
            file.write("## Daten\n")
            
            dataset = self.createMarkDownString("Alle Produkte", "products")
            if self.checkLengthinFile("Accommodation") > 0:
                dataset += self.createMarkDownString("Unterkünfte", "Accommodation")
            if self.checkLengthinFile("CivicStructure") > 0:
                dataset += self.createMarkDownString("CivicStructure", "CivicStructure")
            if self.checkLengthinFile("AdministrativeArea") > 0:
                dataset += self.createMarkDownString("AdministrativeArea", "AdministrativeArea")
            if self.checkLengthinFile("TransportationSystem") > 0:
                dataset += self.createMarkDownString("TransportationSystem", "TransportationSystem")
            if self.checkLengthinFile("LocalBusiness") > 0:
                dataset += self.createMarkDownString("LocalBusiness", "LocalBusiness")
            if self.checkLengthinFile("FoodEstablishment") > 0:
                dataset += self.createMarkDownString("FoodEstablishment", "FoodEstablishment")
            if self.checkLengthinFile("LodgingBusiness") > 0:
                dataset += self.createMarkDownString("LodgingBusiness", "LodgingBusiness")
            if self.checkLengthinFile("Tour") > 0:
                dataset += self.createMarkDownString("Tour", "Tour")
            if self.checkLengthinFile("Webcam") > 0:
                dataset += self.createMarkDownString("Webcam", "Webcam")
            if self.checkLengthinFile("Event") > 0:
                dataset += self.createMarkDownString("Event", "Event")
            if self.checkLengthinFile("Product") > 0:
                dataset += self.createMarkDownString("Product", "Product")
            if self.checkLengthinFile("CreativeWork") > 0:
                dataset += self.createMarkDownString("CreativeWork", "CreativeWork")
            if self.checkLengthinFile("MediaObject") > 0:
                dataset += self.createMarkDownString("MediaObject", "MediaObject")
            file.write(dataset)
            
        print(f"Markdown file created at: {markdown_file_path}")
        
    def createMarkDownFileDocumentation(self):
        # Load the documentation.md file from the load package folder
        documentation_file_path = os.path.join(os.path.dirname(__file__), "documentation.md")
        target_file_path = os.path.join(self.projectPath, "documentation.md")
        
        if os.path.exists(documentation_file_path):
            with open(documentation_file_path, "r", encoding='utf-8') as source_file:
                content = source_file.read()
            
            with open(target_file_path, "w", encoding='utf-8') as target_file:
                target_file.write(content)
            
            print(f"Documentation file copied to: {target_file_path}")
        else:
            print(f"Documentation file not found at: {documentation_file_path}")