import json
import os
from datetime import datetime
from contentdeskopendata.load.geojson import GeoJsonTransformer
from contentdeskopendata.load.map import mapCreator
from contentdeskopendata.load.openApiConf import OpenApiConf
from contentdeskopendata.load.changelog import ChangeLogMaker

class Load:
    
    def __init__(self, transformProducts, projectPath, organization, name, website, organization_website, email, region, license):
        self.projectPath = projectPath
        self.organization = organization
        self.name = name
        self.website = website
        self.organization_website = organization_website
        self.email = email
        self.region = region
        self.license = license
        self.transformProducts = transformProducts
        self.countProducts = len(self.transformProducts)
        self.typesClass = self.loadAllTypes()
        self.loadProducts = self.setLoadProducts()
        self.createMarkDownFileIndex()
        self.createMarkDownFileDocumentation()
        self.createMarkDownChangelogFiles()
        self.createMarkDownFileChangelogMain()
        self.createOpenApiConf()
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
        
        objectPlace = self.createProductListbyParentTyp("Place")
        self.loadFormats(objectPlace, "Place", "Place")
        objectAccommodation = self.createProductListbyParentTyp("Accommodation")
        self.loadFormats(objectAccommodation, "Accommodation", "Accommodation")
        objectCivicStructure = self.createProductListbyParentTyp("CivicStructure")
        self.loadFormats(objectCivicStructure, "CivicStructure", "CivicStructure")
        objectAdministrativeArea = self.createProductListbyParentTyp("AdministrativeArea")
        self.loadFormats(objectAdministrativeArea, "AdministrativeArea", "AdministrativeArea")
        objectTransportationSystem = self.createProductListbyParentTyp("TransportationSystem")
        self.loadFormats(objectTransportationSystem, "TransportationSystem", "TransportationSystem")
        objectLocalBusiness = self.createProductListbyParentTyp("LocalBusiness")
        self.loadFormats(objectLocalBusiness, "LocalBusiness", "LocalBusiness")
        FoodEstablishment = self.createProductListbyParentTyp("FoodEstablishment")
        self.loadFormats(FoodEstablishment, "FoodEstablishment", "FoodEstablishment")
        objectLodgingBusiness = self.createProductListbyParentTyp("LodgingBusiness")
        self.loadFormats(objectLodgingBusiness, "LodgingBusiness", "LodgingBusiness")
        objectTour = self.createProductListbyParentTyp("Tour")
        self.loadFormats(objectTour, "Tour", "Tour")
        objectWebcam = self.createProductListbyParentTyp("Webcam")
        self.loadFormats(objectWebcam, "Webcam", "Webcam")
        objectEvent = self.createProductListbyParentTyp("Event")
        self.loadFormats(objectEvent, "Event", "Event")
        objectProduct = self.createProductListbyParentTyp("Product")
        self.loadFormats(objectProduct, "Product", "Product")
        objectCreativeWork = self.createProductListbyParentTyp("CreativeWork")
        self.loadFormats(objectCreativeWork, "CreativeWork", "CreativeWork")
        objectMediaObject = self.createProductListbyParentTyp("MediaObject")
        self.loadFormats(objectMediaObject, "MediaObject", "MediaObject")

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
        geojsonProducts = GeoJsonTransformer().setProductsToGeoJson(products)

        self.createRSSFeed(rssProducts, fileName)
        self.createCSV(csvProducts, fileName)
        self.createGeoJson(geojsonProducts, fileName)
        
        self.mapCreator = mapCreator("/api/"+fileName+".geojson", fileName, self.projectPath).createMap(self.projectPath+"/map/"+fileName+".html")

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
                if 'de' in product['description']:
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
    
    def createGeoJson(self, products, fileName):
        # Check if folder exists
        print("Folder Path: ", self.projectPath+"/api/"+fileName+".geojson")
        if not os.path.exists(self.projectPath+"/api/"):
            os.makedirs(self.projectPath+"/api/")

        with open(self.projectPath+"/api/"+fileName+".geojson", "w", encoding="utf-8") as file:
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
    
    def createMarkDownString(self, name, filename, count):
        string = ""
        
        #string += "["+name+" ("+str(count)+")](/api/"+filename+".json)\n\n"

        string += "| ["+name+" ("+str(count)+")](/api/"+filename+".json)       | [:material-code-json:](/api/"+filename+".json){ .md-button } [:fontawesome-solid-file-csv:](/api/"+filename+".csv){ .md-button } [:simple-rss:](/api/"+filename+".rss){ .md-button }  | [:material-map-marker:](/map/"+filename+".html){ .md-button } |\n"
        
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
    
    def splitStringtoList(self, string):
        newstring = ''
        # Split the string by commas and strip whitespace
        items = [item.strip() for item in string.split(',') if item.strip()]
        for item in items:
            if item:
                newstring += '* '+item + '\n'
        return newstring
    
    def createOpenApiConf(self):
        openapiConfig = OpenApiConf.getOpenApiConfig(self.organization, self.website)
        # create a openapi.json file in the projectPath
        openapi_file_path = os.path.join(self.projectPath, "openapi.json")
        with open(openapi_file_path, "w", encoding='utf-8') as file:
            file.write(json.dumps(openapiConfig, ensure_ascii=False, indent=2))
        print(f"OpenAPI file created at: {openapi_file_path}")        
    
    def createMarkDownFileIndex(self):
        # create a markdown file with the name "data.md" in the projectPath
        markdown_file_path = os.path.join(self.projectPath, "index.md")
        with open(markdown_file_path, "w", encoding='utf-8') as file:
            file.write("---\n")
            file.write("hide:\n")
            file.write("  - navigation\n")
            file.write("  - toc\n")
            file.write("description: Hier finden Sie öffentlich zugängliche touristische Datensätze wie Unterkünfte, Erlebnisse und Gastronomiebetriebe, bereitgestellt von "+self.organization+".\n")
            file.write("---\n")
            file.write("# OpenData Portal - "+self.organization+"\n\n")
            #file.write(str(self.countProducts)+ " freie Datensätze\n\n")
            file.write("Die hier veröffentlichten Daten stehen kostenlos zur Verfügung und können mit einer [CC BY-SA](https://creativecommons.org/licenses/by-sa/4.0/deed.de) Lizenz frei wiederverwendet werden. \n\n")
            #file.write("[Dokumentation](documentation)\n\n")
            file.write("## Was ist Open Data?\n\n")
            file.write("„Open Data“ bedeutet: Daten, die frei zugänglich, kostenlos nutzbar und von jedem weiterverwendet werden dürfen – ganz ohne komplizierte Bedingungen.\n\n")
            file.write("## Wozu dient dieses Portal?\n")
            
            file.write("Dieses Portal richtet sich an:\n\n")
            file.write(" * **Reiseveranstalter, Hotels und Touristiker**, die aktuelle Informationen zu Veranstaltungen, Ausflugszielen oder Unterkünften suchen,\n")
            file.write(" * **Medien, Entwickler oder Startups**, die auf Basis der Daten neue Anwendungen oder Angebote entwickeln möchten,\n")
            file.write(" * **interessierte Bürgerinnen und Bürger**, die einen Einblick in die touristische Vielfalt der Region erhalten möchten.\n\n")
         
            file.write("## Was finde ich hier?\n\n")
            file.write("Sie finden unter anderem Daten zu:\n\n")
            file.write("* 📍 **Punkten**, wie Unterkünfte, Restaurants oder Ausflugsziele\n")
            file.write("* 🗺️ **Linien**, wie Routen und Touren\n")
            file.write("* 📅 **Events**, wie Messen, Sportveranstaltungen, uvm.\n")
            file.write("* 📰 **Artikel**, wie News, Produkte o.ä.\n")
            file.write("* 📷 **Medien**, wie Webcams, Bilder, Videos o.ä.\n")
            file.write("Diese Daten stammen direkt von unseren touristischen Partnern und werden regelmässig aktualisiert.\n\n")
            
            file.write("## Wie kann ich die Daten nutzen?\n\n")
            file.write("* Wenn Sie möchten, können Sie die Daten herunterladen.\n")
            file.write("* Sie dürfen die Daten in eigene Projekte, Websites oder Broschüren einbauen - die Daten dürfen:\n\n")
            file.write("✅ vervielfältigt, verbreitet und öffentlich zugänglich gemacht werden\n\n")
            file.write("✅ angereichert und bearbeitet werden\n\n")
            file.write("✅ kommerziell genutzt werden\n\n")

            #file.write("## Lizenz\n")
            #file.write(self.splitStringtoList(self.license))
            #file.write("\n\n")
            file.write("## "+str(self.countProducts)+" freie Datensätze\n")

            file.write("| Daten      | Format                           | Ansehen\n")
            file.write("| ----------- | --------------------------------| ----------- |\n")

            dataset = self.createMarkDownString("Alle Produkte", "products", self.checkLengthinFile("products"))
            if self.checkLengthinFile("Place") > 0:
                dataset += self.createMarkDownString("Orte", "Place", self.checkLengthinFile("Place"))
            #if self.checkLengthinFile("Accommodation") > 0:
            #    dataset += self.createMarkDownString("Unterkünfte", "Accommodation", self.checkLengthinFile("Accommodation"))
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
            # if self.checkLengthinFile("Product") > 0:
            #    dataset += self.createMarkDownString("Produkte", "Product", self.checkLengthinFile("Product"))
            # if self.checkLengthinFile("CreativeWork") > 0:
            #    dataset += self.createMarkDownString("Kreative Arbeit", "CreativeWork", self.checkLengthinFile("CreativeWork"))
            # if self.checkLengthinFile("MediaObject") > 0:
            #    dataset += self.createMarkDownString("Medienobjekt", "MediaObject", self.checkLengthinFile("MediaObject"))
            file.write(dataset)
            file.write("\n\n")
            file.write("### Haftungsausschluss\n\n")
            file.write("* "+self.organization+" schliesst jede Haftung für direkte und indirekte Schäden durch die Datennutzung aus. Es wird keine Garantie für die Aktualität, Richtigkeit, Vollständigkeit und Genauigkeit der veröffentlichten Daten übernommen.\n\n")
            
            file.write("## Noch Fragen?\n\n")
            file.write("Weitere Informationen sind in der Entwicklerdokumentation zu finden:\n\n")
            file.write("* [📒 Dokumentation](documentation)\n\n")
            file.write("* [📄 Changelog ](changelog)\n\n")
            file.write("Wenn Sie unsicher sind, wie Sie die Daten nutzen können oder weitere Informationen wünschen, melden Sie sich gerne bei uns:\n\n")
            file.write("* 📧 [E-Mail](mailto:"+str(self.email)+")\n")
            
        print(f"Markdown file created at: {markdown_file_path}")
        
    def createMarkDownFileDocumentation(self):
        # create a markdown file with the name "documentation.md" in the projectPath
        markdown_file_path = os.path.join(self.projectPath, "documentation.md")
        with open(markdown_file_path, "w", encoding='utf-8') as file:
            file.write("---\n")
            file.write("hide:\n")
            file.write("  - navigation\n")
            #file.write("  - toc\n")
            file.write("---\n\n")
            file.write("# Documentation\n\n")
            
            file.write("## Introduction\n\n")
            file.write("This document describes the open data API of /api for retrieving information about places and accommodation locations published on the site. Each of these entities are also tagged with one or more categories. The following objects can be retrieved via the API:\n\n")
            file.write("* Places like restaurants, museums, points of interest\n")
            file.write("* Accommodations\n\n")
            
            file.write("## API Endpoints\n\n")
            file.write("The main endpoint of the API is located at [/api](/api). The API can be used to retrieve all the available categories, or to retrieve all the objects tagged with a specific category.\n\n")
            
            file.write("## Categories list\n\n")
            file.write("By just calling the endpoint, [/api/category.json](/api/category.json), without any other parameters, the result is a list of all the available categories. The category items are stored as a hierarchical tree, so each of the category items has also a reference to its parent. If the parent is \"null\", then the category is a root item. An excerpt from the result list can be seen below:\n\n")
            file.write("```json\n")
            file.write("{\"code\":\"sui_01\",\"parent\":\"sui_root\",\"labels\":{\"de_CH\":\"Aktivitäten\",\"en_US\":\"Activities\",\"fr_FR\":\"Activités\",\"it_IT\":\"Attività\"}}\n")
            file.write("```\n\n")
            
            file.write("## Objects list\n\n")
            file.write("By appending the path of a category to the API endpoint, you can get all the objects which are tagged with that respective category. For example, to get all the objects tagged with category LodgingBusiness, the following path can be used /api/LodgingBusiness.json. The result would be a list of all the LodgingBusiness, for example:\n\n")
            file.write("```json\n")
            file.write("{\"@context\":\"http://schema.org\",\"@type\":\"Place\",\"identifier\":\"84d386b3-5fd5-4c8f-ad6a-0958086fb50d\",\"category\":[\"sui_01\",\"sui_0101\"],\"dateCreated\":\"2021-06-16T14:04:14+02:00\",\"dateModified\":\"2022-06-20T22:19:49+02:00\",\"name\":{\"de_CH\":\"Swissyurt\",\"en_US\":\"Swissyurt\",\"fr_FR\":\"Swissyurt\",\"it_IT\":\"Swissyurt\"},\"disambiguatingDescription\":{\"de_CH\":\"Die liebevoll selbst gebaute Jurte \\u00abSwissyurt\\u00bb ausserhalb von Bischofszell ist eine kleine runde Oase, um die Seele baumeln zu lassen. Für Entdeckerinnen und Naturliebhaber! \"},\"description\":{\"de_CH\":\"Das von den Gastgebern selbst errichtete \\u00abZelt\\u00bb, das seinen Ursprung bei den Nomaden in Zentralasien hat, beherbergt auf rund 20 Quadratmetern bis zu vier Personen. Eingerichtet ist die Swissyurt ähnlich einem kleinen Studio – nur mit einer Prise mehr Abenteuer. So kocht man etwa auf einem zweiflammigen Gasrechaud vor dem Eingang und heizt an kälteren Tagen mit einem Holzofen. \\n\\nAuf der Terrasse geniesst man einen herrlichen Blick auf die Flusslandschaft der Sitter und ist umgeben von Wiesen, Wald und Feldern. Ein kleiner Holzkohlengrill lädt zum sommerlichen Grillplausch, ein Spielplatz zum Schaukeln und Wippen. Ein eigenes WC und Dusche befinden sich im 30 Meter entfernten Wohnhaus. \"},\"license\":\"cc0\",\"address\":{\"addressCountry\":\"ch\",\"addressLocality\":\"Bischofszell / Eberswil\",\"postalCode\":\"9220\",\"streetAddress\":\"Eberswilerstrasse 15 A\",\"telephone\":\"+41 71 422 12 15\",\"email\":\"swissyurt@gmail.com\",\"url\":\"http://swissyurt.business.site/?utm_source=tgt.pim.tso.ch\\u0026utm_medium=Standard\\u0026utm_campaign=DestinationData\\u0026utm_source=ost.pim.tso.ch\\u0026utm_medium=Standard\\u0026utm_campaign=DestinationData\"},\"geo\":{\"@type\":\"GeoCoordinates\",\"latitude\":\"47.5017361\",\"longitude\":\"9.2613015\"},\"openstreetmap_id\":\"6284663052\",\"google_place_id\":\"ChIJpWbCvHvkmkcRt6XfVtCVjQw\",\"image\":\"https://ostpimtsoch.sos-ch-dk-2.exoscale-cdn.com/catalog/1/b/3/d/1b3dda6a4a5e1b03eb7b9a0330cf2e4c6e6a603e_04f5b6aa4bb81856fcdc1207994010d7.JPG\",\"Opens\":[\"Friday\",\"Monday\",\"Saturday\",\"Sunday\",\"Thursday\",\"Tuesday\",\"Wednesday\"]}\n")
            file.write("```\n\n")
            
            file.write("## Translations\n\n")
            file.write("Some of the fields support translations. For those fields, the returned value is actually an object containing the language codes as properties and the actual field, translated in that language, as value. The fields which do not support translations will just return their value directly. As an example in the above snippet, the openingDays field does not support translations, while the name supports it.\n\n")
            
            file.write("## Schema.org and discover.swiss integration\n\n")
            file.write("Some of the returned fields in the objects are also schema.org standard. The @type attribute of the objects identifies the schema.org type, and can have the following values:\n\n")
            file.write("* LodgingBusiness for accommodations [https://schema.org/LodgingBusiness](https://schema.org/LodgingBusiness).\n")
            file.write("* Place for places [https://schema.org/Place](https://schema.org/Place).\n")
            file.write("* LocalBusiness for restaurants / cafes [https://schema.org/LocalBusiness](https://schema.org/LocalBusiness).\n\n")
            file.write("Full Types list can be found at [Types](https://docs.discover.swiss/dev/concepts/content-organization/types-and-additionaltypes/).\n\n")
            
            file.write("## Non-standard fields\n\n")
            file.write("There are, however, a few custom fields which are not schema.org standard. The full list of non-standard fields, per each object type, can be seen below.\n\n")
            file.write("Available on all the types:\n\n")
            file.write("* openstreetmap_id: the OpenStreetMap ID of the object.\n")
            file.write("* google_place_id: the Google Place ID of the object.\n")
            file.write("* discoverSwissId: the Discover Swiss ID of the object.\n")
            
            file.write("## Change log\n\n")
            file.write("* [Version 2.0 ](/changelog)\n\n")

            file.write("## License\n\n")
            file.write("The data published here is available free of charge and can be freely reused under a CC BY-SA license. The data may be:\n\n")
            file.write("* Reproduced, disseminated and made available to others.\n")
            file.write("* Augmented and edited.\n")
            file.write("* Used commercially.\n")
        
        print(f"Markdown file created at: {markdown_file_path}")

    def createMarkDownChangelogFiles(self):
        ChangeLogMaker().copyAllChangelogfromReproURL()
        
    def createMarkDownFileChangelogMain(self):
        markdown_file_path = os.path.join(self.projectPath, "changelog.md")
        with open(markdown_file_path, "w", encoding='utf-8') as file:
            file.write("---\n")
            file.write("hide:\n")
            file.write("  - navigation\n")
            #file.write("  - toc\n")
            file.write("---\n\n")
            file.write("# Change log\n\n")
            file.write("[Version 2.1](CHANGELOG-2.1.md)\n\n")
            file.write("[Version 2.0](CHANGELOG-2.0.md)\n\n")
        print(f"Markdown file created at: {markdown_file_path}")

    def createMarkDownFileChangelog(self):
        markdown_file_path = os.path.join(self.projectPath, "changelog.md")
        with open(markdown_file_path, "w", encoding='utf-8') as file:
            file.write("---\n")
            file.write("hide:\n")
            file.write("  - navigation\n")
            #file.write("  - toc\n")
            file.write("---\n\n")
            file.write("# Change log\n\n")
            file.write("Version 2.0\n\n")

            file.write("## Change for description field\n\n")
            file.write("The description field got an upgrade to a full wysiwyg field with the following allowed tags: &lt;em&gt;&lt;strong&gt;&lt;code&gt;&lt;ul&gt;&lt;ol&gt;&lt;li&gt;&lt;dl&gt;&lt;dt&gt;&lt;dd&gt;&lt;h2&gt;&lt;h3&gt;&lt;h4&gt;&lt;h5&gt;&lt;h6&gt;&lt;img&gt;&lt;h1&gt;&lt;pre&gt;&lt;p&gt;&lt;a&gt;&lt;table&gt;&lt;caption&gt;&lt;/caption&gt;&lt;tbody&gt;&lt;thead&gt;&lt;tfoot&gt;&lt;th&gt;&lt;td&gt;&lt;tr&gt;&lt;br&gt;.\n\n")
            file.write("In Open Data V1 there were just &lt;p&gt; tags allowed.\n\n")

            file.write("## More possible values in the @type field\n\n")
            file.write("The @type field can now have more values than just LodgingBusiness and Place. The full list of possible values is:\n\n")
            file.write(" [Types](https://docs.discover.swiss/dev/concepts/content-organization/types-and-additionaltypes/) of discover.swiss\n\n")

            file.write("## More possible properties \n\n")
            file.write("The following properties are now available in the API:\n\n")
            file.write("* [priceRange](https://schema.org/priceRange)\n")
            file.write("* [starRating](https://schema.org/starRating)\n")
            file.write("* [openingHoursSpecification](https://schema.org/openingHoursSpecification)\n")
            file.write("* [openingHours](https://schema.org/openingHours)\n")
            file.write("* [amenityFeature](https://schema.org/amenityFeature)\n")
            file.write("* [award](https://schema.org/award)\n")
            file.write("* [offers](https://schema.org/offers)\n")
            file.write("* [paymentAccepted](https://schema.org/paymentAccepted)\n")
            file.write("* [currenciesAccepted](https://schema.org/currenciesAccepted)\n")
            file.write("* [checkinTime](https://schema.org/checkinTime)\n")
            file.write("* [checkoutTime](https://schema.org/checkoutTime)\n")
            file.write("* [petsAllowed](https://schema.org/petsAllowed)\n")
            file.write("* [numberOfRooms](https://schema.org/numberOfRooms)\n")
            file.write("* [maximumAttendeeCapacity](https://schema.org/maximumAttendeeCapacity)\n")
                
            file.write("### Image\n\n")
            file.write("Image is now delivered with type ImageObject and the properties “caption”. \n\n")
                
            file.write("## Category\n\n")
            file.write("The category is now delivered with the disocvers.wiss categories and their IDs. [/api/category.json](/api/category.json)")
                
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
