import shutil
from contentdeskopendata.load.mapHtml import mapHtml

class mapCreator:
    def __init__(self, geojsonPath, name, projectPath):
        self.geojsonPath = geojsonPath
        self.name = name
        self.projectPath = projectPath

    def createMap(self, output_path):
        # Copy the template file
        
        #map = os.path.join(self.projectPath, "map/products.html")
        map = mapHtml.get_map_html()

        # Replace the <title> tag content
        map = map.replace('<title> Alle Produkte </title>', f'<title>{self.name}</title>')
        # Replace the geojson filename in the script tag
        map = map.replace(
            "var geojsonURL = '/api/products.geojson'",
            f"var geojsonURL = '/api/{self.name}.geojson'"
        )

        # Write the modified content back
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(map)