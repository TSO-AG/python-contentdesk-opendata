class GeoJsonTransformer:
    def __init__(self):
        pass

    def setGeoJsonData(self, product):
        geojson_feature = {
            "type": "Feature",
        }
        
        geojson_feature["properties"] = {}
        if isinstance(product, dict) and "identifier" in product:
            geojson_feature["properties"]['identifier'] = product["identifier"]
        if 'name' in product and 'de' in product["name"]:
            geojson_feature["properties"]['name'] = product["name"]['de']
        if 'description' in product and 'de' in product["description"]:
            geojson_feature["properties"]['description'] = product["description"]["de"]
        if 'address' in product:
            if 'url' in product['address']:
                geojson_feature["properties"]['url'] = product['address']['url']
        if 'image' in product:
            geojson_feature["properties"]['image'] = product['image'][0]['contentUrl']
        if 'additionalProperty' in product and 'openstreetmap_id' in product['additionalProperty']:
            geojson_feature["properties"]['openstreetmap_id'] = product['additionalProperty']['openstreetmap_id']

        if 'geo' in product and 'latitude' in product['geo'] and 'longitude' in product['geo']:
            geojson_feature["geometry"] = {
                    "type": "Point",
                    "coordinates": [product['geo']['longitude'], product['geo']['latitude']]
            }
        return geojson_feature

    def setProductsToGeoJson(self, products):
        # Transform the GeoJSON data as needed
        geojson_data = {
            'type': 'FeatureCollection',
            'features': []
        }   
        for product in products:
            geojson_feature = self.setGeoJsonData(product)
            geojson_data["features"].append(geojson_feature)
            
        return geojson_data