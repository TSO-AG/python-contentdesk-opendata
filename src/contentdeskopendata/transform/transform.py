import json
import os

class Transform:
    
    def __init__(self, extractProducts, projectPath, cdnurl):
        self.projectPath = projectPath
        self.extractProducts = extractProducts
        self.cdnurl = cdnurl
        self.typesClass = self.loadAllTypes()
        self.categories = self.loadCategories()
        self.transformProducts = self.transformToJSONLD()

    def transformToJSONLD(self):
        jsonLD = []
        for product in self.extractProducts:
            newProduct = self.setProductJSONLD(product)
            jsonLD.append(newProduct)
        return jsonLD
    
    def license(self, code):
        if code == 'cc0':
            return 'CC0'
        elif code == 'ccby':
            return 'CC BY'
        elif code == 'ccbync':
            return 'CC BY-NC'
        elif code == 'ccbynd':
            return 'CC BY-ND'
        elif code == 'ccbysa':
            return 'CC BY-SA'
        elif code == 'ccbyncnd':
            return 'CC BY-NC-ND'
        elif code == 'ccbyncsa':
            return 'CC BY-NC-SA'
        else:
            return None
        
    def loadCategories(self):
        category_file_path = os.path.join(self.projectPath, "category.json")
        print("Category File Path: ", category_file_path)
        if os.path.exists(category_file_path):
            with open(category_file_path, "r") as file:
                categories = json.load(file)
            return categories
        else:
            print(f"File {category_file_path} does not exist.")
            return []
        
    def getCategoriesbyList(self, categories):
        categoriesList = {}
        for category in categories:
            print("Category: ", category)
            if category in self.categories:
                categoryKey = str(self.categories[category]['labels']['en_US'])
                categoriesList[categoryKey] = {}
                categoriesList[categoryKey]['suiId'] = category
                
        print("Categories List: ", categoriesList)
        return categoriesList
    
    def getTransformProducts(self):
        return self.transformProducts
    
    def getCdnUrl(self):
        return self.cdnurl
    
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

    def getParentTypeByType(self, type):
        parentType = next((t['parent'] for k, t in self.typesClass.items() if k == type), None)
        return parentType
    
    def setProductJSONLD(self, product):
        newProduct = {}
        newProduct['@context'] = "http://schema.org/"
        newProduct['@type'] = product["family"]
        if self.getParentTypeByType(product["family"]):
            newProduct['additionalType'] = self.getParentTypeByType(product["family"])
        newProduct['identifier'] = product["identifier"]
        if 'leisure' in product['values'] and product['values']['leisure']:
            newProduct['category'] = self.getCategoriesbyList(product['values']['leisure'][0]['data'])
        #newProduct['dateCreated'] = product['created']
        newProduct['dateModified'] = product['updated']
        # Generel
        if 'name' in product["values"]:
            newProduct['name']= self.languageToJSONLD(product["values"]['name'])
        if 'disambiguatingDescription' in product["values"]:
            newProduct['disambiguatingDescription'] = self.languageToJSONLD(product["values"]['disambiguatingDescription']) 
        if 'description' in product["values"]:
            newProduct['description'] = self.languageToJSONLD(product["values"]['description'])
        if 'license' in product["values"]:
            newProduct['license'] = self.license(product["values"]["license"][0]['data'])
        # Address
        if 'addressLocality' in product['values']:
            newProduct['address'] = self.setAddress(product)
        # Geo
        if 'latitude' in product['values']:
            geo = {}
            geo['@type'] = 'GeoCoordinates'
            geo['latitude'] = product['values']['latitude'][0]['data']
            if 'longitude' in product['values']:
                geo['longitude'] = product['values']['longitude'][0]['data']
            newProduct['geo'] = geo
        # Images
        if 'image' in product['values']:
            # TODO: Image Group / Array with Gallery-Images
            newProduct['image'] = []
            newImage = {}
            newImage['@type'] = 'ImageObject'
            newImage['contentUrl'] = self.cdnurl + product['values']['image'][0]['data']
            if 'image_description' in product['values']:
                newImage['caption'] = self.languageToJSONLD(product['values']['image_description'])
            newProduct['image'].append(newImage)
        
        # TODO: Photos
            
        if 'copyrightHolder' in product['values']:
            newProduct['copyrightHolder'] = product['values']['copyrightHolder'][0]['data']
        
        # priceRange
        if 'priceRange' in product['values']:
            newProduct['priceRange'] = self.setPriceRange(product)
        
        if 'starRating' in product['values']:
            newProduct['starRating'] = {}
            newProduct['starRating']['@type'] = 'Rating'
            newProduct['starRating']['ratingValue'] = product['values']['starRating'][0]['data']
            
        if 'openingHours' in product['values']:
            newProduct['openingHours'] = self.languageToJSONLD(product['values']['openingHours'])
            
        if 'openingHoursSpecification' in product['values']:
            # TODO: Split openingHoursSpecification to specialOpeningHoursSpecification
            newProduct['openingHoursSpecification'] = product['values']['openingHoursSpecification'][0]['data']
            # TODO: set specialOpeningHoursSpecification
            #newProduct['specialOpeningHoursSpecification'] = product['values']['specialOpeningHoursSpecification'][0]['data']
            
        if 'amenityFeature' in product['values']:
            newProduct['amenityFeature'] = self.setAmenityFeature(product)
        
        if 'servesCuisine' in product['values']:
            newProduct['servesCuisine'] = self.setservesCuisine(product)
        
        if 'award' in product['values']:
            newProduct['award'] = self.setAward(product)
            
        if 'publicAccess' in product['values']:
            newProduct['publicAccess'] = product['values']['publicAccess'][0]['data']
        
        if 'isAccessibleForFree' in product['values']:
            newProduct['isAccessibleForFree'] = product['values']['isAccessibleForFree'][0]['data']
            
        if 'offers' in product['values']:
            newProduct['offers'] = {}
            newProduct['offers']['@type'] = 'Offer'
            newProduct['offers']['description'] = self.languageToJSONLD(product['values']['offers'])
            if 'price' in product['values']:
                newProduct['offers']['price'] = product['values']['price'][0]['data']
            #TODO: Variants in Products
            
        if 'paymentAccepted' in product['values']:
            newProduct['paymentAccepted'] = product['values']['paymentAccepted'][0]['data']
        
        if 'currenciesAccepted' in product['values']:
            newProduct['currenciesAccepted'] = product['values']['currenciesAccepted'][0]['data']
        
        if 'checkinTime' in product['values']:
            newProduct['checkinTime'] = product['values']['checkinTime'][0]['data']
            
        if 'checkoutTime' in product['values']:
            newProduct['checkoutTime'] = product['values']['checkoutTime'][0]['data']
            
        if 'petsAllowed' in product['values']:
            newProduct['petsAllowed'] = product['values']['petsAllowed'][0]['data']
        
        if 'numberOfRooms' in product['values']:
            newProduct['numberOfRooms'] = product['values']['numberOfRooms'][0]['data']
            
        if 'maximumAttendeeCapacity' in product['values']:
            newProduct['maximumAttendeeCapacity'] = product['values']['maximumAttendeeCapacity'][0]['data']
        
        # additionalProperty tbd'
        additional_properties = {}
        
        if 'openstreetmap_id' in product['values']:
            additional_properties['openstreetmap_id'] = product['values']['openstreetmap_id'][0]['data']
        if 'google_place_id' in product['values']:
            additional_properties['googlePlaceId'] = product['values']['google_place_id'][0]['data']
        if 'discoverId' in product['values']:
            additional_properties['discoverSwissId'] = product['values']['discoverId'][0]['data']
        
        if additional_properties:
            newProduct['additionalProperty'] = additional_properties
        
        # Associations
        ## MeetingRoom
        if 'MeetingRoom' in product['associations']:
            if len(product['associations']['MeetingRoom']['products']) > 0:
                newProduct['containsPlace'] = self.setcontainsPlace(product)
                
        ## Video
        if 'video' in product['associations']:
            if len(product['associations']['video']['products']) > 0:
                newProduct['video'] = self.setVideoObject(product)

        return newProduct
    
    def languageToJSONLD(self, languageValue):
        product = {}
        for language in languageValue:
            local = language['locale']
            prefixLocale = local.split('_')[0]
            product[prefixLocale] = {}
            nameValue = language['data']
            product[prefixLocale] = nameValue
            
        return product
    
    def setAddress(self, product):
        if 'addressLocality' in product['values']:
            address = {}
            address['@type'] = 'PostalAddress'
            address['addressLocality'] = product['values']['addressLocality'][0]['data']
            if 'addressCountry' in product['values']:
                address['addressCountry'] = {}
                address['addressCountry']['@type'] = 'Country'
                address['addressCountry']['name'] = product['values']['addressCountry'][0]['data']
            if 'addressRegion' in product['values']:
                address['addressRegion'] = product['values']['addressRegion'][0]['data']
            if 'postalCode' in product['values']:
                address['postalCode'] = product['values']['postalCode'][0]['data']
            if 'streetAddress' in product['values']:
                address['streetAddress'] = product['values']['streetAddress'][0]['data']
            if 'telephone' in product['values']:
                address['telephone'] = product['values']['telephone'][0]['data']
            if 'email' in product['values']:
                address['email'] = product['values']['email'][0]['data']
            if 'url' in product['values']:
                address['url'] = product['values']['url'][0]['data']
        else:
            address = None
        return address
    
    def setPriceRange(self, product):
        priceRange = []
        for price in product['values']['priceRange'][0]['data']:
            newPrice = price.split('_')
            if len(newPrice) == 2:
                priceRange.append(newPrice[1])
            else:
                priceRange.append(newPrice[0])
            
        return priceRange
    
    def setAmenityFeature(self, product):
        amenityFeature = []
        for amenity in product['values']['amenityFeature'][0]['data']:
            newAmenity = {}
            newAmenity['@type'] = 'LocationFeatureSpecification'
            # TODO: amenityFeature Label 
            newAmenity['name'] = amenity
            newAmenity['value'] = True
            amenityFeature.append(newAmenity)
            
        return amenityFeature
    
    def setservesCuisine(self, product):
        servesCuisine = []  
        for cuisine in product['values']['servesCuisine'][0]['data']:
            newCuisine = {}
            # TODO: amenityFeature Label
            newCuisine['name'] = cuisine
            servesCuisine.append(newCuisine)
        return servesCuisine

    def setAward(self, product):
        award = []
        for awardValue in product['values']['award'][0]['data']:
            newAward = {}
            #newAward['@type'] = 'Certification'
            #TODO: award Label
            newAward['name'] = awardValue
            award.append(newAward)
            
        return award
    
    def setcontainsPlace(self, product):
        containsPlace = []
        # add MeetingRoom
        if 'associations' in product and 'MeetingRoom' in product['associations']:
            meetingRooms = self.setMeetingRoom(product)
            containsPlace.extend(meetingRooms)
            
        return containsPlace
    
    def setMeetingRoom(self, product):
        meetingRoom = []
        for room in product['associations']['MeetingRoom']['products']:
            roomObject = self.getProductById(room)
            newRoom = {}
            newRoom['@type'] = 'MeetingRoom'
            newRoom['identifier'] = room
            if 'name' in roomObject['values']:
                newRoom['name'] = self.languageToJSONLD(roomObject['values']['name'])
            if 'disambiguatingDescription' in roomObject['values']:
                newRoom['disambiguatingDescription'] = self.languageToJSONLD(roomObject['values']['disambiguatingDescription'])
            if 'description' in roomObject['values']:
                newRoom['description'] = self.languageToJSONLD(roomObject['values']['description'])
                
            if 'floorSize' in roomObject['values']:
                newRoom['floorSize'] = {}
                newRoom['floorSize']['@type'] = 'QuantitativeValue'
                newRoom['floorSize']['value'] = roomObject['values']['floorSize'][0]['data']
                if 'floorSize_unit' in roomObject['values']:
                    newRoom['floorSize']['unitCode'] = roomObject['values']['floorSize_unit'][0]['data']
            if 'maximumAttendeeCapacity' in roomObject['values']:
                newRoom['maximumAttendeeCapacity'] = roomObject['values']['maximumAttendeeCapacity'][0]['data']
            if 'amenityFeature' in roomObject['values']:
                newRoom['amenityFeature'] = self.setAmenityFeature(roomObject)
            if 'occupancy' in roomObject['values']:
                newRoom['occupancy'] = {}
                newRoom['occupancy']['@type'] = 'QuantitativeValue'
                newRoom['occupancy']['value'] = roomObject['values']['occupancy'][0]['data']
                if 'occupancy_unit' in roomObject['values']:
                    newRoom['occupancy']['unitCode'] = roomObject['values']['occupancy_unit'][0]['data']
            meetingRoom.append(newRoom)
            
        return meetingRoom
    
    def setVideoObject(self, product):
        if 'associations' in product and 'video' in product['associations']:
            videos = []
            for video in product['associations']['video']['products']:
                videoObject = self.getProductById(video)
                newVideo = {}
                if videoObject:
                    newVideo['@type'] = 'VideoObject'
                    newVideo['identifier'] = video
                    if 'name' in videoObject['values']:
                        newVideo['name'] = self.languageToJSONLD(videoObject['values']['name'])
                    if 'contentUrl' in videoObject['values']:
                        newVideo['contentUrl'] = videoObject['values']['contentUrl'][0]['data']
                    if 'thumbnailUrl' in videoObject['values']:
                        newVideo['thumbnailUrl'] = videoObject['values']['thumbnailUrl'][0]['data']
                    if 'embedUrl' in videoObject['values']:
                        newVideo['embedUrl'] = videoObject['values']['embedUrl'][0]['data']
                videos.append(newVideo)

        return videos

    def getProductById(self, identifier):
        for product in self.extractProducts:
            if product['identifier'] == identifier:
                return product
        return None