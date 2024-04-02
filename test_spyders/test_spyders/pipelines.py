# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
from dotenv import load_dotenv
from itemadapter import ItemAdapter
import json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


# Get passwords
load_dotenv()
db_password = os.getenv("DB_PASSWORD")
uri = f"mongodb+srv://AI:{db_password}@cluster0.gtl6qtn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client:MongoClient = MongoClient(uri, server_api=ServerApi('1'))
db = client['db-data']


class TestSpydersPipeline:
    authors = []
    quotes = []

    def process_item(self, item, spider):
        if spider.name == 'authors':
            adapter = ItemAdapter(item)
            if 'fullname' in adapter.keys():
                self.authors.append(dict(adapter))
            else:
                raise Exception('---------------AuthorsSpider: Something went wrong')   

        elif spider.name == 'quotes':
            adapter = ItemAdapter(item)
            if 'quote' in adapter.keys():
                self.quotes.append(dict(adapter))
            else:
                raise Exception('---------------QuotesSpider: Something went wrong')   

        else:
            return item 
        
    def close_spider(self, spider):
        if spider.name == 'authors':
            with open('authors.json', 'w', encoding='utf8') as f:
                json.dump(self.authors, f, ensure_ascii=False, indent=4)
                db['authors'].insert_many(self.authors)

        elif spider.name == 'quotes':
            with open('quotes.json', 'w', encoding='utf8') as f:
                json.dump(self.quotes, f, ensure_ascii=False, indent=4)
                db['quotes'].insert_many(self.quotes) 

        else:
            pass
