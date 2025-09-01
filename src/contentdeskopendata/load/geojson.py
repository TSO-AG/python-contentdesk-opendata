class GeoJsonTransformer:
    def __init__(self, products):
        self.products = products

    def setGeoJsonData(self, product):
        geojson_feature = {
            "type": "Feature",
            "properties": {
                "identifier": product["identifier"],
                "name": product["name"]['de'],
                "description": product["description"]["de"],
                "url": product['address']['url'],
                "image": product['image'][0]['contentUrl'],
                "openstreetmap_id": product['additionalProperty']['openstreetmap_id']
            },
            "geometry": {
                "type": "Point",
                "coordinates": [product['geo']['longitude'], product['geo']['latitude']]
            },
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