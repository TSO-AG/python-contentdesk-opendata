
class mapHtml:
    def getMapHtml():
        return """
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
        <title> Alle Produkte </title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
        <link rel="icon" href="/assets/favicon-180-180.png">
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" integrity="sha512-xodZBNTC5n17Xt2atTPuE1HxjVMSvLVW9ocqUKLsCC5CXdbqCmblAshOMAS6/keqq/sMZMZ19scR4PsZChSR7A==" crossorigin="" />
        <link rel="stylesheet" href="/stylesheets/L.Control.Sidebar.css" />
        <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js" integrity="sha512-XQoYMqMTK8LvdxXYG3nZ448hOEQiglfqkJs1NOQV44cWnUrBc8PkAOcXy20w0vlaXaVUearIOBhiXZ5V3ynxwA==" crossorigin=""></script>
        <style>
            html, body {
                height: 100%;
                margin: 0;
            }
            .leaflet-container {
                height: 400px;
                width: 600px;
                max-width: 100%;
                max-height: 100%;
            }
        </style>
        <style>
            body { 
                padding: 0; margin: 0; 
            } 
            #map { 
                height: 100%; 
                width: 100vw; 
            }
        </style>
        <script>
            var geojsonURL = '/api/products.geojson'
        </script>
    </head>
  <body>
    <div id="map"></div>
    <div id="sidebar">
        <h1>Name</h1>
        <img src="" width="100%" class="img-fluid">
    </div>
    <script src="/javascripts/L.Control.Sidebar.js" type="text/javascript"></script>
    <script type="text/javascript">
        var centerview=[47.2773,9.2258];
        var mymap = L.map('map').setView([centerview[0], centerview[1]], 10);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(mymap);

        async function load_shapefile() {
            const geojsonURL = window.geojsonURL;
            console.log(geojsonURL);
            let url = geojsonURL;
            const response = await fetch(url)
            const shape_obj = await response.json();
            console.log(shape_obj);
            return shape_obj;
        }

        async function main() {
            const json = await load_shapefile();
            //L.geoJson(json).addTo(mymap);
            // Popup
            const geojsonLayer = L.geoJSON(json, {
                onEachFeature: function (feature, layer) {
                    layer.bindPopup('<h1>'+feature.properties.name+'</h1><img src="'+feature.properties.image+'" width="100%" /><p><a href="'+feature.properties.url+'">Webseite</a>');
                    //layer.bindTooltip('<h1>'+feature.properties.name+'</h1><img src="'+feature.properties.image+'" width="100%" /><p><a href="'+feature.properties.url+'">Webseite</a>');
                    }
                }).addTo(mymap);
            // Sidebar
            /*L.geoJSON(json, {
                onEachFeature: function (feature, layer) {
                    layer.on('click', function () {
                            sidebar.toggle();
                        });
                    }
                }).addTo(mymap);
            */
            const bounds = geojsonLayer.getBounds();
            
            if (bounds.isValid()) {
                map.fitBounds(bounds, {
                    padding: [50, 50],          // Innenabstand zum Rand (Pixel)
                    maxZoom: 15,               // Obergrenze, damit nicht zu stark gezoomt wird
                    animate: true,
                    duration: 0.8              // Animationsdauer in Sekunden
                });
            } else {
                console.warn('GeoJSON enthält keine gültigen Geometrien.');
            }
        }

        var sidebar = L.control.sidebar('sidebar', {
            closeButton: true,
            position: 'right'
        });
        mymap.addControl(sidebar);

        mymap.on('click', function () {
            sidebar.hide();
        })

        main();
    </script>
  </body>
</html>
"""
