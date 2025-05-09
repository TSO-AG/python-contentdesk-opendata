---
hide:
  - navigation
---

# Documentation

## Introduction

This document describes the open data API of opendata.ziggy.pim.tso.ch for retrieving information about places and accommodation locations published on the site. Each of these entities are also tagged with one or more categories. The following objects can be retrieved via the API:

* Places like restaurants, museums, points of interest
* Accommodations

## API Endpoints

The main endpoint of the api is located at /api. The API can be used to retrieve all the available categories, or to retrieve all the objects tagged with a specific category.

## Categories list

By just calling the endpoint, /api/category, without any other parameters, the result is a list of all the available categories. The category items are stored as a hierarchical tree, so each of the category item has also a reference to its parent. If the parent is "null", then the category is a root item. An excerpt from the result list can be seen bellow:

``` json
{"code":"ostschweiz_unterkuenfte","parent":"ostschweiz","labels":{"de_CH":"Unterk\u00fcnfte","en_US":"Accommodation","fr_FR":"H\u00e9bergement","it_IT":"Alloggio"}}
```

The parent represents the code of the parent for the category item. If "null", the category is a root item. The name represents the actual name or label of the category (this is a translatable field) and the path contains the location where all the objects tagged with the respective category item can be found.

## Objects list

By appending the path of a category to the API endpoint, you can get all the objects which are tagged with that respective category. For example, to get all the objects tagged with ziggy_unterkuenfte, the following path can be used /api/category/ziggy_unterkuenfte. The result would be a list of all the Accommodation, for example:

``` json
{"@context":"http://schema.org","@type":"Place","identifier":"84d386b3-5fd5-4c8f-ad6a-0958086fb50d","category":["ostschweiz_ferienwohnung","ostschweiz_unterkuenfte","ostschweiz_unterkuenfte_aussergewoehnlich"],"dateCreated":"2021-06-16T14:04:14+02:00","dateModified":"2022-06-20T22:19:49+02:00","name":{"de_CH":"Swissyurt","en_US":"Swissyurt","fr_FR":"Swissyurt","it_IT":"Swissyurt"},"disambiguatingDescription":{"de_CH":"Die liebevoll selbst gebaute Jurte \u00abSwissyurt\u00bb ausserhalb von Bischofszell ist eine kleine runde Oase, um die Seele baumeln zu lassen. F\u00fcr Entdeckerinnen und Naturliebhaber! "},"description":{"de_CH":"Das von den Gastgebern selbst errichtete \u00abZelt\u00bb, das seinen Ursprung bei den Nomaden in Zentralasien hat, beherbergt auf rund 20 Quadratmetern bis zu vier Personen. Eingerichtet ist die Swissyurt \u00e4hnlich einem kleinen Studio \u2013 nur mit einer Prise mehr Abenteuer. So kocht man etwa auf einem zweiflammigen Gasrechaud vor dem Eingang und heizt an k\u00e4lteren Tagen mit einem Holzofen. \n\nAuf der Terrasse geniesst man einen herrlichen Blick auf die Flusslandschaft der Sitter und ist umgeben von Wiesen, Wald und Feldern. Ein kleiner Holzkohlengrill l\u00e4dt zum sommerlichen Grillplausch, ein Spielplatz zum Schaukeln und Wippen. Ein eigenes WC und Dusche befinden sich im 30 Meter entfernten Wohnhaus. "},"license":"cc0","address":{"addressCountry":"ch","addressLocality":"Bischofszell / Eberswil","postalCode":"9220","streetAddress":"Eberswilerstrasse 15 A","telephone":"+41 71 422 12 15","email":"swissyurt@gmail.com","url":"http://swissyurt.business.site/?utm_source=tgt.pim.tso.ch\u0026utm_medium=Standard\u0026utm_campaign=DestinationData\u0026utm_source=ost.pim.tso.ch\u0026utm_medium=Standard\u0026utm_campaign=DestinationData"},"geo":{"@type":"GeoCoordinates","latitude":"47.5017361","longitude":"9.2613015"},"openstreetmap_id":"6284663052","google_place_id":"ChIJpWbCvHvkmkcRt6XfVtCVjQw","image":"https://ostpimtsoch.sos-ch-dk-2.exoscale-cdn.com/catalog/1/b/3/d/1b3dda6a4a5e1b03eb7b9a0330cf2e4c6e6a603e_04f5b6aa4bb81856fcdc1207994010d7.JPG","Opens":["Friday","Monday","Saturday","Sunday","Thursday","Tuesday","Wednesday"]}
```

## Translations

Some of the fields support translations. For those fields, the returned value is actually an object containing the language codes as properties and the actual field, translated in that language, as value. The fields which do not support translations will just return their value directly. As an example in the above snipped, the openingDays field does not support translations, while the name supports it.

## Schema.org integration

Some of the returned fields in the objects are also schema.org standard. The @type attribute of the objects identifies the schema.org type, and can have the following values

* LodgingBusiness for accommodations (https://schema.org/LodgingBusiness).
* Place for places (https://schema.org/Place).
* LocalBusiness for restaurants / cafes (https://schema.org/LocalBusiness).

## Non-standard fields

There are, however, a few custom fields which are not schema.org standard. The full list of non-standard fields, per each object type, can be seen bellow.

Available on all the types:

* category: a list of categories this object is tagged with on the site.

## License

The data published here is available free of charge and can be freely reused under a CC BY-SA license. The data may be:

* Reproduced, disseminated and made available to others.
* Augmented and edited.
* Used commercially.

