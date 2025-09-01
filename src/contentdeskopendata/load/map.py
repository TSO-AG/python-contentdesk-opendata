import shutil
import os

class mapCreator:
    def __init__(self, geojsonPath, name, projectPath):
        self.geojsonPath = geojsonPath
        self.name = name
        self.projectPath = projectPath

    def createMap(self, output_path):
        # Copy the template file
        
        map = os.path.join(self.projectPath, "map/products.html")
            
        shutil.copy(map, output_path)

        # Read the copied file and modify Title and geoJsonUrL
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Replace the <title> tag content
        content = content.replace('<title> Alle Produkte </title>', f'<title>{self.name}</title>')
        # Replace the geojson filename in the script tag
        content = content.replace(
            "var geojsonURL = '/api/products.geojson'",
            f"var geojsonURL = '/api/{self.name}.geojson'"
        )

        # Write the modified content back
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)