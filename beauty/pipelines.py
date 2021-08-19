import re
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class SplitPostalCodeLocation:
    """Split zip_city into postalcode and location"""
    def process_item(self, item, spider):
        pattern = r'(?P<postalcode>\d+)\s+(?P<location>.+)'
        ma = re.search(pattern, item.get('zip_city', ''))
        if ma:
            item['postalcode'] = ma.group('postalcode')
            item['location'] = ma.group('location')
            del item['zip_city']
        return item 
        

class SplitServices:
    """Split string of services to proper list"""
    def process_item(self, item, spider):
        services = item['services'].split(',')
        services = [service.strip() for service in services]
        item['services'] = services
        return item 
    

class AddLeadingZeroToPostalcode:
    """Add a leading zero to an incorrect German postalcode"""
    def process_item(self, item, spider):
        if (
            item['countrycode'] == 'DE' and 
            len(item['postalcode']) == 4
        ):
            item['postalcode'] = f"0{item['postalcode']}"
        return item


class FilterIncompleteAddress:
    """Remove items with an incomplete address"""
    def process_item(self, item, spider):
        if all(
            (
                item.get('postalcode'), 
                item.get('location'), 
                item.get('street')
            )
        ):
            return item
        else:
            raise DropItem(
                f'Incomplete address for {item.get("url")}'
            )

class FilterDuplicates:
    """Remove duplicate items based on URL"""
    def __init__(self):
        self.urls_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['url'] in self.urls_seen:
            raise DropItem(
                f"Duplicate item {adapter['url']}"
            )
        else:
            self.urls_seen.add(adapter['url'])
            return item
