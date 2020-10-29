import scrapy
import re
from db_creation import Yarn, db

# # TODO: Automate pagination


class KokonkiHimalayaSpider(scrapy.Spider):
    name = "kokonkiHimalaya"
    start_urls = [
        'https://kokonki.pl/wloczka-himalaya-dolphin-baby/1',
        'https://kokonki.pl/wloczka-himalaya-dolphin-baby/2/',
        'https://miladruciarnia.pl/pl/c/Doplhin-Baby/99',
        'https://amicrafts.pl/pl/c/Dolphin-Baby/380',
        'https://amicrafts.pl/pl/c/Dolphin-Baby/380/2',
        'https://kokonki.pl/pl/c/Kulka-silikonowa/206',
        'https://miladruciarnia.pl/pl/c/Kulka-silikonowa%2C-wypelnienie/182',
        'https://amicrafts.pl/pl/c/Wypelnienie/122'
        'https://kokonki.pl/pl/searchquery/kulka/1/phot/5?url=kulka',
        'https://miladruciarnia.pl/pl/searchquery/kulka/1/phot/5?url=kulka',
        'https://amicrafts.pl/pl/searchquery/kulka/1/phot/5?url=kulka'
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

            query = Yarn.select().where(Yarn.url == url)
            if not query.exists():
                item = Yarn.create(name=name, price=price, availability=availability, number=number, page=page, url=url)
                item.save()
            else:
                query = Yarn.update(price=price, availability=availability).where(Yarn.url == url)
                query.execute()

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
