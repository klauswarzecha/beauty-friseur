import time
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule
from beauty.items import BeautyItem
from beauty.items import BeautyItemLoader

from fake_useragent import UserAgent


class KosmetikSpider(CrawlSpider):
    name = 'kosmetik'
    allowed_domains = ['kosmetik.com']
    
    _firstpage = 1
    _lastpage = 5720

    start_urls = [
        f'https://www.kosmetik.com/firmen/page/{page}/' 
        for page in range(_firstpage, _lastpage)
    ]
    
    custom_settings = {
        'AUTOTHROTTLE_TARGET_CONCURRENCY' : 16, 
    } 

    _useragent = UserAgent(verify_ssl=False)
    # cf. https://github.com/hellysmile/fake-useragent/issues/53

    rules = ( 
        Rule(
            LinkExtractor(
                allow=(
                    r'/firmen/(page/\d+/)?', 
                ),
                allow_domains=('kosmetik.com'), 
                restrict_xpaths=(
                    (
                        '//div[@class="jlinkadress_list"]'
                        '/form'
                    ), 
                ),
            ),
            callback='parse_city', 
            follow=True, 
        ),
    )

    def parse_city(self, response):
        """Return individual items for each cosmetics parlor in a city"""

        parlors = response.xpath(
            (
                '//div[@class="jlinkadress_list"]'
                '/form[@id="adminForm"]'
                '/div[contains(@class, "row")]'
            )
        )
        for parlor in parlors:  
            
            ldr = BeautyItemLoader(item=BeautyItem())
            
            business_block = parlor.xpath('./div[2]')
            service_block = parlor.xpath('./div[3]')
            rating_block = parlor.xpath('./div[4]')
            
            services = service_block.xpath('././text()').get()
            anchor = business_block.xpath(
                './h2/a[@class="firma_title"]'
            )
            company_name = anchor.xpath('./@title').get()
            url = anchor.xpath('./@href').get()
            
            address_raw = business_block.xpath('./text()').getall()

            try:
                zip_city = address_raw[-1]
            except IndexError:
                zip_city = None
            
            try:
                street = address_raw[-2]
            except IndexError:
                street = None
            
            rating_raw = rating_block.xpath(
                (
                    './div[@class="rating_div"]'
                    '/div[@class="post-ratings"]'
                    '/img[1]/@alt'
                 )
            ).get()
            try:
                rating_parts = rating_raw.split()
            except AttributeError:
                pass
            else:
                rating_count = rating_parts[0]
                rating_mean = rating_parts[3]
                rating_mean = rating_mean.replace(',', '.')
                ldr.add_value('rating_mean', rating_mean)
                ldr.add_value('rating_count', rating_count)
            
            ldr.add_value('portal', 'kosmetik')
            ldr.add_value('timestamp', time.time())
            ldr.add_value('url', url)
            ldr.add_value('company_name', company_name)
            ldr.add_value('street', street)
            ldr.add_value('zip_city', zip_city)
            ldr.add_value('countrycode', 'DE')
            ldr.add_value('services', services)
            yield ldr.load_item()
