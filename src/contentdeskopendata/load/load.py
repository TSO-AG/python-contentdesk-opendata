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
        self.copyFileCategory()
               
    def getLoadProducts(self):
        return self.transformProducts
    
    def setLoadProducts(self):
        # All Products to api/products.json
        self.loadProductsToFile(self.transformProducts, "products")
        self.loadFormats(self.transformProducts, "products", "Alle Daten")
        
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
        self.loadFormats(self.transformProducts, "Place", "Place")
        self.createProductListbyParentTyp("Accommodation")
        self.loadFormats(self.transformProducts, "Accommodation", "Accommodation")
        self.createProductListbyParentTyp("CivicStructure")
        self.loadFormats(self.transformProducts, "CivicStructure", "CivicStructure")
        self.createProductListbyParentTyp("AdministrativeArea")
        self.loadFormats(self.transformProducts, "AdministrativeArea", "AdministrativeArea")
        self.createProductListbyParentTyp("TransportationSystem")
        self.loadFormats(self.transformProducts, "TransportationSystem", "TransportationSystem")
        self.createProductListbyParentTyp("LocalBusiness")
        self.loadFormats(self.transformProducts, "LocalBusiness", "LocalBusiness")
        self.createProductListbyParentTyp("FoodEstablishment")
        self.loadFormats(self.transformProducts, "FoodEstablishment", "FoodEstablishment")
        self.createProductListbyParentTyp("LodgingBusiness")
        self.loadFormats(self.transformProducts, "LodgingBusiness", "LodgingBusiness")
        self.createProductListbyParentTyp("Tour")
        self.loadFormats(self.transformProducts, "Tour", "Tour")
        self.createProductListbyParentTyp("Webcam")
        self.loadFormats(self.transformProducts, "Webcam", "Webcam")
        self.createProductListbyParentTyp("Event")
        self.loadFormats(self.transformProducts, "Event", "Event")
        self.createProductListbyParentTyp("Product")
        self.loadFormats(self.transformProducts, "Product", "Product")
        self.createProductListbyParentTyp("CreativeWork")
        self.loadFormats(self.transformProducts, "CreativeWork", "CreativeWork")
        self.createProductListbyParentTyp("MediaObject")
        self.loadFormats(self.transformProducts, "MediaObject", "MediaObject")
        
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
        
        with open(self.projectPath+"/api/"+fileName+".json", "w", encoding="utf-8") as file:
            file.write(json.dumps(products))
    
    def loadFormats(self, products, fileName, title):
        # Check if folder exists
        
        rssProducts = self.generateRSSFeed(products, fileName, title)
        csvProducts = self.generateCSV(products)
        
        self.createRSSFeed(rssProducts, fileName)
        self.createCSV(csvProducts, fileName)
    
    def generateCSV(self, products):
        csvProducts = ""
        csvProducts += "id;name;disambiguatingDescription;description;longitude;latitude;streetAddress;postalCode;addressLocality;telephone;email;url;image;dateModified"

        for item in products:
            csvProducts += item['identifier']+";"+item['name']['de']+";"
            if 'disambiguatingDescription' in item:
                if 'de' in item['disambiguatingDescription']:
                    csvProducts += item['disambiguatingDescription']['de']+";"
                else:
                    csvProducts += ";"
            if 'description' in item:
                if 'de' in item['description']:
                    csvProducts += item['description']['de']+";"
                else:
                    csvProducts += ";"
            if 'geo' in item:
                if 'longitude' in item['geo']: 
                    csvProducts += item['geo']['longitude']+";"+item['geo']['latitude']+";"
            if 'address' in item:
                if 'streetAddress' in item['address']:
                    csvProducts += item['address']['streetAddress']+";"
                if 'postalCode' in item['address']:
                    csvProducts += item['address']['postalCode']+";"
                if 'addressLocality' in item['address']:
                    csvProducts += item['address']['addressLocality']+";"
                if 'telephone' in item['address']:
                    csvProducts += item['address']['telephone']+";"
                if 'email' in item['address']:
                    csvProducts += item['address']['email']+";"
                if 'url' in item['address']:
                    csvProducts += item['address']['url']+";"
            if 'image' in item:
                csvProducts += str(item['image'])+";"
            csvProducts += item['dateModified']+"\n"

        return csvProducts
    
    
    def generateRSSFeed(self, products, fileName, title):
        rssFeed = '<rss version="2.0">'
        rssFeed += '<channel>'
        rssFeed += '<title>'+ self.name + ' - '+ title +'</title>'
        rssFeed += '<link>'+ self.website +'/api/'+fileName+'.rss</link>'
        rssFeed += '<language>de</language>'
        rssFeed += '<docs>'+ self.website +'/api/</docs>'
        rssFeed += '<generator>Contentdesk.io</generator>'
        for product in products:
            rssFeed += '<item>'
            rssFeed += '<title>'+ str(product['name']['de']) +'</title>'
            if 'address' in product:
                if 'url' in product['address']:
                    rssFeed += '<link>'+ product['address']['url'] +'</link>'
            else:
                rssFeed += '<link>'+ self.organization_website +'</link>'
            if 'description' in product:
                rssFeed += '<description>'+ str(product['description']['de']) +'</description>'
            if 'image' in product:
                rssFeed += '<enclosure length="" type="image/jpeg" url="'+ str(product['image'][0]['contentUrl']) +'" />'
            rssFeed += '<guid isPermaLink="false">'+ product['identifier'] +'</guid>'
            rssFeed += '<pubDate>'+ product['dateModified'] +'</pubDate>'
        
        rssFeed += '</channel>'
        rssFeed += '</rss>'
        return rssFeed
    
    def createRSSFeed(self, products, fileName):
        # Check if folder exists
        print("Folder Path: ", self.projectPath+"/api/"+fileName+".rss")
        if not os.path.exists(self.projectPath+"/api/"):
            os.makedirs(self.projectPath+"/api/")
        
        with open(self.projectPath+"/api/"+fileName+".rss", "w", encoding="utf-8") as file:
            file.write(products)
    
    def createCSV(self, products, fileName):
        # Check if folder exists
        print("Folder Path: ", self.projectPath+"/api/"+fileName+".csv")
        if not os.path.exists(self.projectPath+"/api/"):
            os.makedirs(self.projectPath+"/api/")
        
        with open(self.projectPath+"/api/"+fileName+".csv", "w", encoding="utf-8") as file:
            file.write(products)
           
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
    
    def createMarkDownString(self, name, filename, count):
        string = ""
        
        #string += "["+name+" ("+str(count)+")](/api/"+filename+".json)\n\n"

        string += "| ["+name+" ("+str(count)+")](/api/"+filename+".json)       | [:material-code-json:](/api/"+filename+".json) [:fontawesome-solid-file-csv:](/api/"+filename+".csv) [:simple-rss:](/api/"+filename+".rss)  |\n"
        
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
            file.write("[Dokumnetation](documentation)\n\n")
            file.write("**Die Daten dürfen**\n\n")
            file.write("- vervielfältigt, verbreitet und weiter zugänglich gemacht werden\n- angereichert und bearbeitet werden\n- kommerziell genutzt werden\n\n")
            file.write("**Haftungsausschluss**\n\n")
            file.write("- Die "+self.organization+" schliesst jede Haftung für direkte und indirekte Schäden durch die Datennutzung aus. Sie übernimmt keine Garantie für die Aktualität, Richtigkeit, Vollständigkeit und Genauigkeit der veröffentlichten Daten.\n\n")
            file.write("## Datensätze\n")
            
            file.write("| Daten      | Format                          |\n")
            file.write("| ----------- | ------------------------------------ |\n")
            
            dataset = self.createMarkDownString("Alle Produkte", "products", self.checkLengthinFile("products"))
            if self.checkLengthinFile("Place") > 0:
                dataset += self.createMarkDownString("Orte", "Place", self.checkLengthinFile("Place"))
            if self.checkLengthinFile("Accommodation") > 0:
                dataset += self.createMarkDownString("Unterkünfte", "Accommodation", self.checkLengthinFile("Accommodation"))
            if self.checkLengthinFile("CivicStructure") > 0:
                dataset += self.createMarkDownString("Öffentliche Anlage/Einrichtung", "CivicStructure", self.checkLengthinFile("CivicStructure"))
            if self.checkLengthinFile("AdministrativeArea") > 0:
                dataset += self.createMarkDownString("Verwaltungsgebiet", "AdministrativeArea", self.checkLengthinFile("AdministrativeArea"))
            if self.checkLengthinFile("TransportationSystem") > 0:
                dataset += self.createMarkDownString("Transportsystemstation", "TransportationSystem", self.checkLengthinFile("TransportationSystem"))
            if self.checkLengthinFile("LocalBusiness") > 0:
                dataset += self.createMarkDownString("Lokale Geschäfte / Freizeit / Dienstleistung", "LocalBusiness", self.checkLengthinFile("LocalBusiness"))
            if self.checkLengthinFile("FoodEstablishment") > 0:
                dataset += self.createMarkDownString("Gastronomie", "FoodEstablishment", self.checkLengthinFile("FoodEstablishment"))
            if self.checkLengthinFile("LodgingBusiness") > 0:
                dataset += self.createMarkDownString("Beherbergungsbetrieb", "LodgingBusiness", self.checkLengthinFile("LodgingBusiness"))
            if self.checkLengthinFile("Tour") > 0:
                dataset += self.createMarkDownString("Tour", "Tour", self.checkLengthinFile("Tour"))
            if self.checkLengthinFile("Webcam") > 0:
                dataset += self.createMarkDownString("Webcam", "Webcam", self.checkLengthinFile("Webcam"))
            if self.checkLengthinFile("Event") > 0:
                dataset += self.createMarkDownString("Event", "Event", self.checkLengthinFile("Event"))
            if self.checkLengthinFile("Product") > 0:
                dataset += self.createMarkDownString("Produkte", "Product", self.checkLengthinFile("Product"))
            # if self.checkLengthinFile("CreativeWork") > 0:
            #    dataset += self.createMarkDownString("Kreative Arbeit", "CreativeWork", self.checkLengthinFile("CreativeWork"))
            # if self.checkLengthinFile("MediaObject") > 0:
            #    dataset += self.createMarkDownString("Medienobjekt", "MediaObject", self.checkLengthinFile("MediaObject"))
            file.write(dataset)
            
        print(f"Markdown file created at: {markdown_file_path}")
        
    def createMarkDownFileDocumentation(self):
        # create a markdown file with the name "documentation.md" in the projectPath
        markdown_file_path = os.path.join(self.projectPath, "documentation.md")
        with open(markdown_file_path, "w", encoding='utf-8') as file:
            file.write("---\n")
            file.write("hide:\n")
            file.write("  - navigation\n")
            file.write("  - toc\n")
            file.write("---\n\n")
            file.write("# Documentation\n\n")
            file.write("## Introduction\n\n")
            file.write("This document describes the open data API of "+self.website+" for retrieving information about places and accommodation locations published on the site. Each of these entities are also tagged with one or more categories. The following objects can be retrieved via the API:\n\n")
            file.write("* Places like restaurants, museums, points of interest\n")
            file.write("* Accommodations\n\n")
            file.write("## API Endpoints\n\n")
            file.write("The main endpoint of the API is located at [/api](/api). The API can be used to retrieve all the available categories, or to retrieve all the objects tagged with a specific category.\n\n")
            file.write("## Categories list\n\n")
            file.write("By just calling the endpoint, [/api/category](/api/category.json), without any other parameters, the result is a list of all the available categories. The category items are stored as a hierarchical tree, so each of the category items has also a reference to its parent. If the parent is \"null\", then the category is a root item. An excerpt from the result list can be seen below:\n\n")
            file.write("```json\n")
            file.write("{\"code\":\"sui_01\",\"parent\":\"sui_root\",\"labels\":{\"de_CH\":\"Aktivitäten\",\"en_US\":\"Activities\",\"fr_FR\":\"Activités\",\"it_IT\":\"Attività\"}}\n")
            file.write("```\n\n")
            file.write("The parent represents the code of the parent for the category item. If \"null\", the category is a root item. The name represents the actual name or label of the category (this is a translatable field) and the path contains the location where all the objects tagged with the respective category item can be found.\n\n")
            file.write("## Objects list\n\n")
            file.write("By appending the path of a category to the API endpoint, you can get all the objects which are tagged with that respective category. For example, to get all the objects tagged with ziggy_unterkuenfte, the following path can be used /api/category/ziggy_unterkuenfte. The result would be a list of all the Accommodation, for example:\n\n")
            file.write("```json\n")
            file.write("{\"@context\":\"http://schema.org\",\"@type\":\"Place\",\"identifier\":\"84d386b3-5fd5-4c8f-ad6a-0958086fb50d\",\"category\":[\"sui_01\",\"sui_0101\"],\"dateCreated\":\"2021-06-16T14:04:14+02:00\",\"dateModified\":\"2022-06-20T22:19:49+02:00\",\"name\":{\"de_CH\":\"Swissyurt\",\"en_US\":\"Swissyurt\",\"fr_FR\":\"Swissyurt\",\"it_IT\":\"Swissyurt\"},\"disambiguatingDescription\":{\"de_CH\":\"Die liebevoll selbst gebaute Jurte \\u00abSwissyurt\\u00bb ausserhalb von Bischofszell ist eine kleine runde Oase, um die Seele baumeln zu lassen. Für Entdeckerinnen und Naturliebhaber! \"},\"description\":{\"de_CH\":\"Das von den Gastgebern selbst errichtete \\u00abZelt\\u00bb, das seinen Ursprung bei den Nomaden in Zentralasien hat, beherbergt auf rund 20 Quadratmetern bis zu vier Personen. Eingerichtet ist die Swissyurt ähnlich einem kleinen Studio – nur mit einer Prise mehr Abenteuer. So kocht man etwa auf einem zweiflammigen Gasrechaud vor dem Eingang und heizt an kälteren Tagen mit einem Holzofen. \\n\\nAuf der Terrasse geniesst man einen herrlichen Blick auf die Flusslandschaft der Sitter und ist umgeben von Wiesen, Wald und Feldern. Ein kleiner Holzkohlengrill lädt zum sommerlichen Grillplausch, ein Spielplatz zum Schaukeln und Wippen. Ein eigenes WC und Dusche befinden sich im 30 Meter entfernten Wohnhaus. \"},\"license\":\"cc0\",\"address\":{\"addressCountry\":\"ch\",\"addressLocality\":\"Bischofszell / Eberswil\",\"postalCode\":\"9220\",\"streetAddress\":\"Eberswilerstrasse 15 A\",\"telephone\":\"+41 71 422 12 15\",\"email\":\"swissyurt@gmail.com\",\"url\":\"http://swissyurt.business.site/?utm_source=tgt.pim.tso.ch\\u0026utm_medium=Standard\\u0026utm_campaign=DestinationData\\u0026utm_source=ost.pim.tso.ch\\u0026utm_medium=Standard\\u0026utm_campaign=DestinationData\"},\"geo\":{\"@type\":\"GeoCoordinates\",\"latitude\":\"47.5017361\",\"longitude\":\"9.2613015\"},\"openstreetmap_id\":\"6284663052\",\"google_place_id\":\"ChIJpWbCvHvkmkcRt6XfVtCVjQw\",\"image\":\"https://ostpimtsoch.sos-ch-dk-2.exoscale-cdn.com/catalog/1/b/3/d/1b3dda6a4a5e1b03eb7b9a0330cf2e4c6e6a603e_04f5b6aa4bb81856fcdc1207994010d7.JPG\",\"Opens\":[\"Friday\",\"Monday\",\"Saturday\",\"Sunday\",\"Thursday\",\"Tuesday\",\"Wednesday\"]}\n")
            file.write("```\n\n")
            file.write("## Translations\n\n")
            file.write("Some of the fields support translations. For those fields, the returned value is actually an object containing the language codes as properties and the actual field, translated in that language, as value. The fields which do not support translations will just return their value directly. As an example in the above snippet, the openingDays field does not support translations, while the name supports it.\n\n")
            file.write("## Schema.org integration\n\n")
            file.write("Some of the returned fields in the objects are also schema.org standard. The @type attribute of the objects identifies the schema.org type, and can have the following values:\n\n")
            file.write("* LodgingBusiness for accommodations [https://schema.org/LodgingBusiness](https://schema.org/LodgingBusiness).\n")
            file.write("* Place for places [https://schema.org/Place](https://schema.org/Place).\n")
            file.write("* LocalBusiness for restaurants / cafes [https://schema.org/LocalBusiness](https://schema.org/LocalBusiness).\n\n")
            file.write("## Non-standard fields\n\n")
            file.write("There are, however, a few custom fields which are not schema.org standard. The full list of non-standard fields, per each object type, can be seen below.\n\n")
            file.write("Available on all the types:\n\n")
            file.write("* category: a list of categories this object is tagged with on the site.\n\n")
            file.write("## License\n\n")
            file.write("The data published here is available free of charge and can be freely reused under a CC BY-SA license. The data may be:\n\n")
            file.write("* Reproduced, disseminated and made available to others.\n")
            file.write("* Augmented and edited.\n")
            file.write("* Used commercially.\n")
        
        print(f"Markdown file created at: {markdown_file_path}")

    def copyFileCategory(self):
        # copy the file category.json from the projectPath to the api folder
        source = os.path.join(self.projectPath, "category.json")
        destination = os.path.join(self.projectPath, "api", "category.json")
        if os.path.exists(source):
            with open(source, "r") as src_file:
                data = json.load(src_file)
            with open(destination, "w") as dest_file:
                json.dump(data, dest_file)
            print(f"File copied from {source} to {destination}")
        else:
            print(f"Source file {source} does not exist.")
