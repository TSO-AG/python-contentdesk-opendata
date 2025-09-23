---
hide:
    - navigation
    # - toc
---

# Change log

Version 2.0

## Change for description field

The description field got an upgrade to a full wysiwyg field with the following allowed tags: &lt;em&gt;&lt;strong&gt;&lt;code&gt;&lt;ul&gt;&lt;ol&gt;&lt;li&gt;&lt;dl&gt;&lt;dt&gt;&lt;dd&gt;&lt;h2&gt;&lt;h3&gt;&lt;h4&gt;&lt;h5&gt;&lt;h6&gt;&lt;img&gt;&lt;h1&gt;&lt;pre&gt;&lt;p&gt;&lt;a&gt;&lt;table&gt;&lt;caption&gt;&lt;/caption&gt;&lt;tbody&gt;&lt;thead&gt;&lt;tfoot&gt;&lt;th&gt;&lt;td&gt;&lt;tr&gt;&lt;br&gt;.

In Open Data V1 there were just &lt;p&gt; tags allowed.

## More possible values in the @type field

The @type field can now have more values than just LodgingBusiness and Place. The full list of possible values is:

[Types](https://docs.discover.swiss/dev/concepts/content-organization/types-and-additionaltypes/) of discover.swiss

## More possible properties 

The following properties are now available in the API:

* [priceRange](https://schema.org/priceRange)
* [starRating](https://schema.org/starRating)
* [openingHoursSpecification](https://schema.org/openingHoursSpecification)
* [openingHours](https://schema.org/openingHours)
* [amenityFeature](https://schema.org/amenityFeature)
* [award](https://schema.org/award)
* [offers](https://schema.org/offers)
* [paymentAccepted](https://schema.org/paymentAccepted)
* [currenciesAccepted](https://schema.org/currenciesAccepted)
* [checkinTime](https://schema.org/checkinTime)
* [checkoutTime](https://schema.org/checkoutTime)
* [petsAllowed](https://schema.org/petsAllowed)
* [numberOfRooms](https://schema.org/numberOfRooms)
* [maximumAttendeeCapacity](https://schema.org/maximumAttendeeCapacity)
                                
### Image

Image is now delivered with type ImageObject and the properties “caption”. 
                                
## Category

The category is now delivered with the disocvers.wiss categories and their IDs. [/api/category.json](/api/category.json)