import re
import time
from urllib.parse import urljoin
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule
from beauty.items import BeautyItem
from beauty.items import BeautyItemLoader

from fake_useragent import UserAgent

class FriseurSpider(CrawlSpider):
    name = 'friseur'
    allowed_domains = ['friseur.com']
    start_urls = ['https://friseur.com/friseure/staedte']
    _baseurl = 'https://friseur.com'
    rules = (
        Rule(
            LinkExtractor(
                allow=(
                    r'/friseure/(at|ch|de)/[a-z\-]+', 
                ),
                allow_domains=('friseur.com'), 
                restrict_xpaths=(
                    '//div[@class="salondirectory-citylist"]'
                ),
            ),
            callback='parse_city'   
        ),
        
    )

    _useragent = UserAgent(verify_ssl=False)
    # https://github.com/hellysmile/fake-useragent/issues/53

    
    def parse_city(self, response):
        """Return individual items for each hairdresser in a city"""
        pattern = (
            r'(?<=https://friseur\.com/friseure)/'
            r'(?P<countrycode>\w{2})/(?=\w+)'
        )
        ma = re.search(pattern, response.url)
        if ma:
            countrycode = ma.group('countrycode')

        hairdressers = response.xpath(
            '//div[@class="main-content"]'
            '//div[@class="content"]'
            '//a[contains(@class, "salonfinder-list-item")]'
        )
        for hairdresser in hairdressers:
            ldr = BeautyItemLoader(item=BeautyItem())
            relative_url = hairdresser.xpath('./@href').get()
            url = urljoin(self._baseurl, relative_url)
            latitude = hairdresser.xpath('./@data-lat').get()
            longitude = hairdresser.xpath('./@data-lng').get()

            # use for nested xpaths
            details = hairdresser.xpath('./div[@class="details-column"]')
            ratings = hairdresser.xpath('./div[@class="rating-column"]')
            
            company_name = details.xpath(
                './div[@class="headline"]/text()'
            ).get()

            address = details.xpath('./div[@class="address"]')
            street = address.xpath(
                './span[@class="street"]/text()'
            ).get()
            zip_city = address.xpath(
                './span[@class="zip_city"]/text()'
            ).get() 

            contact = details.xpath('./div[@class="contact"]')
            phone = contact.xpath(
                './span[@class="phone"]/text()'
            ).get()

            rating_mean = ratings.xpath(
                './span[@class="rating-outline"]'
                '/span[@class="mean-rating"]/text()'
            ).get()
            rating_count = ratings.xpath(
                './span[@class="rating-as-text"]/text()'
            ).get()

            ldr.add_value('portal', 'friseur')
            ldr.add_value('timestamp', time.time())
            ldr.add_value('url', url)
            ldr.add_value('latitude', latitude)
            ldr.add_value('longitude', longitude)
            ldr.add_value('company_name', company_name)
            ldr.add_value('street', street)
            ldr.add_value('zip_city', zip_city)
            ldr.add_value('phone', phone)
            ldr.add_value('rating_mean', rating_mean)
            ldr.add_value('rating_count', rating_count)
            ldr.add_value('countrycode', countrycode)
            yield ldr.load_item()
