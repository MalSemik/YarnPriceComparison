import scrapy
#TODO: Add what page
#TODO: Automate pagination
#TODO: database

class KokonkiHimalayaSpider(scrapy.Spider):
    name = "kokonkiHimalaya"
    start_urls = [
        'https://kokonki.pl/wloczka-himalaya-dolphin-baby/1',
        'https://kokonki.pl/wloczka-himalaya-dolphin-baby/2/',
        'https://miladruciarnia.pl/pl/c/Doplhin-Baby/99',
        'https://amicrafts.pl/pl/c/Dolphin-Baby/380',
        'https://amicrafts.pl/pl/c/Dolphin-Baby/380/2'
    ]
    def parse(self,response):
        for post in response.css('div.product.s-grid-3.product-main-wrap'):
            yield{
               'name': post.css('.productname::text').get(),
               'price': post.css('.price em::text').get(),
               'availability': post.css('.buttons.f-row fieldset button span::text').get()
            }
        # next_page = response.css('a.next-posts-link::attr(href)').get()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)
