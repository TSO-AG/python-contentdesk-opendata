class OpenApiConf:
    def getOpenApiConfig():
        return {
  "openapi": "3.0.3",
  "info": {
    "title": "ContentDesk OpenData Demo API",
    "description": "Eine OpenAPI‑Spezifikation für das öffentliche JSON‑Feed. Die zurückgelieferten Objekte orientieren sich am schema.org‑Typ.",
    "version": "1.0.0",
    "contact": {
      "name": "ContentDesk Support",
      "url": "https://contentdesk.io",
      "email": "support@contentdesk.io"
    }
  },
  "servers": [
    {
      "url": "https://opendata.demo.contentdesk.io/api",
      "description": "OpenData Demo ContentDesk"
    }
  ],
  "paths": {
    "/products": {
      "get": {
        "summary": "Liste aller Produkte",
        "description": "Ruft das gesamte Produkt‑Dataset im JSON‑Format ab. Jeder Eintrag entspricht dem schema.org‑Typ.",
        "operationId": "listProducts",
        "responses": {
          "200": {
            "description": "Erfolgreiche Rückgabe einer Liste ",
            "content": {
              "application/json": {
                "examples": {
                  "sample": {
                    "summary": "Beispielantwort",
                    "value": [
                      {"@context": "http://schema.org/", "@type": "Motel", "additionalType": "LodgingBusiness", "identifier": "044a580b-dd45-46ea-b845-e1a5ce2b2524", "dateModified": "2025-05-19T08:57:52+02:00", "name": {"de": "Blütenzauber Motel"}, "disambiguatingDescription": {"de": "Charmantes Motel in einem malerischen Dorf, das Gästen gemütliche Unterkünfte und einen herzlichen Empfang bietet. Perfekt für eine entspannende Auszeit vom Alltag."}, "description": {"de": "<p>Das Blütenzauber Motel liegt inmitten eines idyllischen Dorfes und bietet seinen Gästen eine gemütliche Unterkunft in familiärer Atmosphäre. Umgeben von wunderschönen Blumenfeldern, ist das Motel der ideale Rückzugsort für Reisende, die Ruhe und Erholung suchen. Die Zimmer sind komfortabel eingerichtet und bieten moderne Annehmlichkeiten, während das freundliche Personal stets bemüht ist, den Gästen einen angenehmen Aufenthalt zu ermöglichen</p>"}, "license": "CC BY-SA", "address": {"@type": "PostalAddress", "addressLocality": "Teufen", "addressCountry": {"@type": "Country", "name": "ch"}, "addressRegion": "MUSTER", "postalCode": "9053", "streetAddress": "Dorfstrasse 115", "telephone": "+41 71 345 67 89", "email": "info@bluetenzauber-motel.ch", "url": "http://www.bluetenzauber-motel.ch"}, "geo": {"@type": "GeoCoordinates", "latitude": "47.39267706243302", "longitude": "9.396583354479608"}, "image": [{"@type": "ImageObject", "contentUrl": "https://demopimtsoch.sos-ch-dk-2.exoscale-cdn.com/catalog/1/d/5/0/1d50e27b0dd3b76a1b1e27eea17adb9c40518401_charmantes_motel_schweiz_sommermorgen.jpg"}], "copyrightHolder": "TSO AG", "priceRange": ["inexpensive"], "starRating": {"@type": "Rating", "ratingValue": "2"}, "openingHours": {"de": "Betriebsferien: Vom 20. Dezember bis 05. Januar"}, "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "opens": "09:00", "closes": "22:00", "dayOfWeek": "https://schema.org/Monday"}, {"@type": "OpeningHoursSpecification", "opens": "09:00", "closes": "22:00", "dayOfWeek": "https://schema.org/Tuesday"}, {"@type": "OpeningHoursSpecification", "opens": "09:00", "closes": "22:00", "dayOfWeek": "https://schema.org/Wednesday"}, {"@type": "OpeningHoursSpecification", "opens": "09:00", "closes": "22:00", "dayOfWeek": "https://schema.org/Thursday"}, {"@type": "OpeningHoursSpecification", "opens": "09:00", "closes": "22:00", "dayOfWeek": "https://schema.org/Friday"}, {"@type": "OpeningHoursSpecification", "opens": "09:00", "closes": "22:00", "dayOfWeek": "https://schema.org/Saturday"}, {"@type": "OpeningHoursSpecification", "opens": "09:00", "closes": "20:00", "dayOfWeek": "https://schema.org/Sunday"}], "amenityFeature": [{"@type": "LocationFeatureSpecification", "name": "characteristics_familyfriendly", "value": True}], "paymentAccepted": ["americanExpress", "cash", "creditCard", "maestro", "masterCard", "visa"], "currenciesAccepted": ["chf", "eur"], "checkinTime": "14:00", "checkoutTime": "09:00", "petsAllowed": True, "numberOfRooms": "132.0000", "additionalProperty": {"openstreetmap_id": "relation/1683947", "discoverSwissId": "log_s9t_aeeqfiar-ttef-eguq-rief-ubqfsucrcfce"}}
                    ]
                  }
                }
              }
            }
          },
          "default": {
            "description": "Unerwarteter Fehler",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Error"
                }
              }
            }
          }
        },
        "tags": ["Products"]
      }
    }
  },
  "components": {
    "schemas": {
      "ProductArray": {
        "type": "array",
        "items": {
          "$ref": "#/components/schemas/Product"
        }
      },
      "Product": {
        "type": "object",
        "required": ["@context", "@type", "identifier", "name"],
        "properties": {
          "@context": {
            "type": "string",
            "enum": ["https://schema.org/", "http://schema.org/"],
            "description": "Verweis auf das schema.org‑Vokabular."
          },
          "@type": {
            "type": "string",
            "enum": ["Product"],
            "description": "Der Typ des Objekts – immer `Product`."
          },
          "identifier": {
            "type": "string",
            "description": "Eindeutige Kennung des Produkts (kann eine interne ID sein)."
          },
          "name": {
            "type": "string",
            "description": "Name des Produkts."
          },
          "description": {
            "type": "string",
            "description": "Ausführliche Beschreibung des Produkts."
          },
          "image": {
            "type": "array",
            "items": {
              "type": "string",
              "format": "uri",
              "description": "URL zu einem Bild des Produkts."
            }
          },
          "additionalProperty": {
            "type": "array",
            "items": {
              "$ref": "#/components/schemas/PropertyValue"
            },
            "description": "Weitere, beliebige Eigenschaften des Produkts."
          }
        },
        "example": {"@context": "http://schema.org/", "@type": "Motel", "additionalType": "LodgingBusiness", "identifier": "044a580b-dd45-46ea-b845-e1a5ce2b2524", "dateModified": "2025-05-19T08:57:52+02:00", "name": {"de": "Blütenzauber Motel"}, "disambiguatingDescription": {"de": "Charmantes Motel in einem malerischen Dorf, das Gästen gemütliche Unterkünfte und einen herzlichen Empfang bietet. Perfekt für eine entspannende Auszeit vom Alltag."}, "description": {"de": "<p>Das Blütenzauber Motel liegt inmitten eines idyllischen Dorfes und bietet seinen Gästen eine gemütliche Unterkunft in familiärer Atmosphäre. Umgeben von wunderschönen Blumenfeldern, ist das Motel der ideale Rückzugsort für Reisende, die Ruhe und Erholung suchen. Die Zimmer sind komfortabel eingerichtet und bieten moderne Annehmlichkeiten, während das freundliche Personal stets bemüht ist, den Gästen einen angenehmen Aufenthalt zu ermöglichen</p>"}, "license": "CC BY-SA", "address": {"@type": "PostalAddress", "addressLocality": "Teufen", "addressCountry": {"@type": "Country", "name": "ch"}, "addressRegion": "MUSTER", "postalCode": "9053", "streetAddress": "Dorfstrasse 115", "telephone": "+41 71 345 67 89", "email": "info@bluetenzauber-motel.ch", "url": "http://www.bluetenzauber-motel.ch"}, "geo": {"@type": "GeoCoordinates", "latitude": "47.39267706243302", "longitude": "9.396583354479608"}, "image": [{"@type": "ImageObject", "contentUrl": "https://demopimtsoch.sos-ch-dk-2.exoscale-cdn.com/catalog/1/d/5/0/1d50e27b0dd3b76a1b1e27eea17adb9c40518401_charmantes_motel_schweiz_sommermorgen.jpg"}], "copyrightHolder": "TSO AG", "priceRange": ["inexpensive"], "starRating": {"@type": "Rating", "ratingValue": "2"}, "openingHours": {"de": "Betriebsferien: Vom 20. Dezember bis 05. Januar"}, "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "opens": "09:00", "closes": "22:00", "dayOfWeek": "https://schema.org/Monday"}, {"@type": "OpeningHoursSpecification", "opens": "09:00", "closes": "22:00", "dayOfWeek": "https://schema.org/Tuesday"}, {"@type": "OpeningHoursSpecification", "opens": "09:00", "closes": "22:00", "dayOfWeek": "https://schema.org/Wednesday"}, {"@type": "OpeningHoursSpecification", "opens": "09:00", "closes": "22:00", "dayOfWeek": "https://schema.org/Thursday"}, {"@type": "OpeningHoursSpecification", "opens": "09:00", "closes": "22:00", "dayOfWeek": "https://schema.org/Friday"}, {"@type": "OpeningHoursSpecification", "opens": "09:00", "closes": "22:00", "dayOfWeek": "https://schema.org/Saturday"}, {"@type": "OpeningHoursSpecification", "opens": "09:00", "closes": "20:00", "dayOfWeek": "https://schema.org/Sunday"}], "amenityFeature": [{"@type": "LocationFeatureSpecification", "name": "characteristics_familyfriendly", "value": True}], "paymentAccepted": ["americanExpress", "cash", "creditCard", "maestro", "masterCard", "visa"], "currenciesAccepted": ["chf", "eur"], "checkinTime": "14:00", "checkoutTime": "09:00", "petsAllowed": True, "numberOfRooms": "132.0000", "additionalProperty": {"openstreetmap_id": "relation/1683947", "discoverSwissId": "log_s9t_aeeqfiar-ttef-eguq-rief-ubqfsucrcfce"}}
      },
      "PropertyValue": {
        "type": "object",
        "required": ["@type", "name", "value"],
        "properties": {
          "@type": {
            "type": "string",
            "enum": ["PropertyValue"]
          },
          "name": {
            "type": "string",
            "description": "Bezeichner der Eigenschaft."
          },
          "value": {
            "type": "string",
            "description": "Wert der Eigenschaft."
          }
        }
      },
      "Error": {
        "type": "object",
        "properties": {
          "code": {
            "type": "integer",
            "description": "HTTP‑Statuscode."
          },
          "message": {
            "type": "string",
            "description": "Kurzbeschreibung des Fehlers."
          }
        },
        "example": {
          "code": 500,
          "message": "Interner Serverfehler"
        }
      }
    },
    "securitySchemes": {}
  },
  "externalDocs": {
    "description": "Weitere Informationen zu schema.org",
    "url": "https://schema.org"
  }
}