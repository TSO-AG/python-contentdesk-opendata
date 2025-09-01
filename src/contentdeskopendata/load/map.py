import shutil
import os

class mapCreator:
    def __init__(self, geojsonPath, title):
        self.geojsonPath = geojsonPath
        self.title = title

    def createMap(self, output_path):
        # Copy the template file
        shutil.copy(os.path.join(os.path.dirname(__file__), 'map.html'), output_path)

        # Read the copied file and modify Title and geoJsonUrL
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Replace placeholders for Title and geoJsonUrL
        # Replace the <title> tag content
        content = content.replace('<title> Alle Produkte </title>', f'<title>{self.title}</title>')
        # Replace the geojson filename in the script tag
        content = content.replace(
            "var geojsonURL = '/api/products.geojson'",
            f"var geojsonURL = '/api/{self.geojsonPath}'"
        )

        # Write the modified content back
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)