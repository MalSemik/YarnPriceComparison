import scrapy
import re
from peewee import *

db = SqliteDatabase('yarn.db')

class Yarn(Model):
    name = CharField()
    price = FloatField()
    availability = BooleanField()
    number = CharField()
    page = CharField()
    url = CharField()

    class Meta:
        database = db

# TODO: Add what page
# TODO: Automate pagination
# TODO: database
db.connect()
db.create_tables([Yarn])

class KokonkiHimalayaSpider(scrapy.Spider):
    name = "kokonkiHimalaya"
    start_urls = [
        'https://kokonki.pl/wloczka-himalaya-dolphin-baby/1',
        'https://kokonki.pl/wloczka-himalaya-dolphin-baby/2/',
        'https://miladruciarnia.pl/pl/c/Doplhin-Baby/99',
        'https://amicrafts.pl/pl/c/Dolphin-Baby/380',
        'https://amicrafts.pl/pl/c/Dolphin-Baby/380/2',
        #'https://kokonki.pl/pl/searchquery/kulka/1/phot/5?url=kulka',
        #'https://miladruciarnia.pl/pl/searchquery/kulka/1/phot/5?url=kulka',
        #'https://amicrafts.pl/pl/searchquery/kulka/1/phot/5?url=kulka'
    ]

    def parse(self, response):
        for post in response.css('div.product.s-grid-3.product-main-wrap'):
            name = post.css('.productname::text').get()
            price = float(post.css('.price em::text').get().replace('\xa0zł', '').replace(',', '.'))
            page = response.css('.link-logo img::attr(alt)').get()
            url = post.css('.prodname.f-row::attr(href)').get()
            # get the yarn number
            if re.search("3\d\d", name) is not None:
                number = re.search("3\d\d", name).group(0)
            else:
                number = 0

            # get the yarn availability
            if post.css('.buttons.f-row fieldset button span::text').get() == 'Do koszyka':
                availability = True
            else:
                availability = False

            item = Yarn.create(name=name, price=price, availability=availability, number=number, page=page, url=url)
            item.save()
db.close()
            # yield {
            #     'name': name,
            #     'price': price,
            #     'availability': availability,
            #     'number': number,
            #     'page': page,
            #     'url':url,
            # }
       # print(page)

        # next_page = response.css('a.next-posts-link::attr(href)').get()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)
