class GeoJsonTransformer:
    def __init__(self, products):
        self.products = products

    def setGeoJsonData(self, product):
        geojson_feature = {
            "type": "Feature",
        }
        
        geojson_feature["properties"] = {}
        geojson_feature["properties"]['identifier'] = product["identifier"]
        geojson_feature["properties"]['name'] = product["name"]['de']
        if 'description' in product and 'de' in product["description"]:
            geojson_feature["properties"]['description'] = product["description"]["de"]
        geojson_feature["properties"]['url'] = product['address']['url']
        geojson_feature["properties"]['image'] = product['image'][0]['contentUrl']
        geojson_feature["properties"]['openstreetmap_id'] = product['additionalProperty']['openstreetmap_id']

        geojson_feature["geometry"] = {
                "type": "Point",
                "coordinates": [product['geo']['longitude'], product['geo']['latitude']]
        }
        return geojson_feature

    def setProductsToGeoJson(self):
        # Transform the GeoJSON data as needed
        geojson_data = {
            'type': 'FeatureCollection',
            'features': []
        }   
        for product in self.products:
            geojson_feature = self.setGeoJsonData(product)
            geojson_data["features"].append(geojson_feature)
        return geojson_data