# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

class TodostuslibrosPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # Separate publisher and ISBN
        data = adapter['data'].split('/')
        adapter['publisher'] = data[0].strip()
        adapter['isbn'] = data[1].strip()
        adapter.pop('data', None)

        return item

