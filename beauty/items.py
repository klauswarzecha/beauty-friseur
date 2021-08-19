import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Join, Compose, Identity
from scrapy.loader import ItemLoader

def clean_zip_city(word):
    """Remove leading comma and line break from zip_city"""
    return word.lstrip(',').strip()

def clean_rating_count(rating_count):
    """Return just the digits for the rating count"""
    return rating_count.replace('Bewertungen', '')

def clean_services(services):
    """Transform string with services to list"""
    services = services.split(',')
    services = [service.strip() for service in services]    
    return services

class BeautyItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    
    latitude_out = Compose(
        TakeFirst(), 
        float
    )
    
    longitude_out = Compose(
        TakeFirst(), 
        float
    )
    
    rating_count_out = Compose(
        TakeFirst(), 
        clean_rating_count, 
        str.strip, 
        int
    )

    rating_mean_out = Compose(
        TakeFirst(), 
        str.strip, 
        float
    )
    
    zip_city_out = Compose(
        TakeFirst(), 
        clean_zip_city
    )
    
    countrycode_out = Compose(
        TakeFirst(), 
        str.upper
    )
    
    services_out = Compose(
        TakeFirst(), 
        clean_services
    )

class BeautyItem(scrapy.Item):
    """Fields for beauty parlors"""
    company_name = scrapy.Field()
    street = scrapy.Field()
    zip_city = scrapy.Field()
    postalcode = scrapy.Field()
    location = scrapy.Field()
    countrycode = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    url = scrapy.Field()
    phone = scrapy.Field()
    rating_mean = scrapy.Field()
    rating_count = scrapy.Field() 
    portal = scrapy.Field()
    # Identifier for the data source
    timestamp = scrapy.Field()
    # Time when record was crawled 
    # in seconds since the Epoch
    services = scrapy.Field()
