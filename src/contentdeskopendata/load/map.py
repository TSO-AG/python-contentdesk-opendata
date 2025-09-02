import os
from contentdeskopendata.load.mapHtml import mapHtml
from contentdeskopendata.load.mapCss import mapCss
from contentdeskopendata.load.mapJs import mapJs

class mapCreator:
    def __init__(self, geojsonPath, name, projectPath):
        self.geojsonPath = geojsonPath
        self.name = name
        self.projectPath = projectPath

    def createMap(self, output_path):
        # Copy the template file
        
        #map = os.path.join(self.projectPath, "map/products.html")
        map = mapHtml.getMapHtml()
        mapCssContent = mapCss.getMapCss()
        mapJsContent = mapJs.getMapJs()

        # Replace the <title> tag content
        map = map.replace('<title> Alle Produkte </title>', f'<title>{self.name}</title>')
        # Replace the geojson filename in the script tag
        map = map.replace(
            "var geojsonURL = '/api/products.geojson'",
            f"var geojsonURL = '/api/{self.name}.geojson'"
        )
        
        if not os.path.exists(self.projectPath+"/map/"):
            os.makedirs(self.projectPath+"/map/")

        # Write the modified content back
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(map)
            
        if not os.path.exists(self.projectPath+"/javascripts/"):
            os.makedirs(self.projectPath+"/javascripts/")

        # Write the JavaScript content
        with open(self.projectPath+"/javascripts/L.Control.Sidebar.js", 'w', encoding='utf-8') as f:
            f.write(mapJsContent)
        
        with open(self.projectPath+"/stylesheets/L.Control.Sidebar.css", 'w', encoding='utf-8') as f:
            f.write(mapCssContent)

