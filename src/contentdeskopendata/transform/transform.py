import json

class Transform:
    
    def __init__(self, extractProducts, config):
        self.extractProducts = extractProducts
        self.config = config
        self.cdnUrl = config['cdnurl']
        self.transformProducts = self.transformToJSONLD()
    
    def transformToJSONLD(self):
        jsonLD = []
        for product in self.extractProducts:
            newProduct = self.setProductJSONLD(product)
            jsonLD.append(newProduct)
    
        return jsonLD
    
    def getTransformProducts(self):
        return self.transformProducts
    
    def getCdnUrl(self):
        return self.cdnUrl
    
    def setProductJSONLD(self, product):
        newProduct = {}
        newProduct['@context'] = "http://schema.org/"
        newProduct['@type'] = product["family"]
        newProduct['identifier'] = product["identifier"]
        if 'leisure' in product['values'] and product['values']['leisure']:
            newProduct['category'] = product['values']['leisure'][0]['data'] 
        #newProduct['dateCreated'] = product['created']
        newProduct['dateModified'] = product['updated']
        # Generel
        if 'name' in product["values"]:
            newProduct['name']= self.languageToJSONLD(product["values"]['name']) ,
        if 'disambiguatingDescription' in product["values"]:
            newProduct['disambiguatingDescription'] = self.languageToJSONLD(product["values"]['disambiguatingDescription']) 
        if 'description' in product["values"]:
            newProduct['description'] = self.languageToJSONLD(product["values"]['description'])
        if 'license' in product["values"]:
            newProduct['license'] = product["values"]["license"][0]['data']
        # Address
        if 'addressLocality' in product['values']:
            newProduct['address'] = self.setAddress(product)
        # Geo
        if 'latitude' in product['values']:
            geo = {}
            geo['latitude'] = product['values']['latitude'][0]['data']
            if 'longitude' in product['values']:
                geo['longitude'] = product['values']['longitude'][0]['data']
            newProduct['geo'] = geo
        # Images
        if 'image' in product['values']:
            # TODO: Image Group / Array with Gallery-Images
            newProduct['image'] = []
            newProduct['image'].append({
                "@type": "ImageObject",
                "contentUrl": self.cdnUrl + product['values']['image'][0]['data']
            })
            
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
    
    def setAward(self, product):
        award = []
        for awardValue in product['values']['award'][0]['data']:
            newAward = {}
            #newAward['@type'] = 'Certification'
            #TODO: award Label
            newAward['name'] = awardValue
            award.append(newAward)
            
        return award