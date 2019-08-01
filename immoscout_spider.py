import scrapy
import datetime

class ImmoscoutSpider(scrapy.Spider):
    name = "immoscout"
    custom_settings = {
        'DOWNLOAD_DELAY' : 0.25
    }

    def start_requests(self):
        urls = ['https://www.immobilienscout24.de/Suche/S-T/Wohnung-Miete/Berlin/Berlin?enteredFrom=one_step_search',
                'https://www.immobilienscout24.de/Suche/S-T/Wohnung-Kauf/Berlin/Berlin?enteredFrom=one_step_search']
        #urls = ['https://www.immobilienscout24.de/Suche/S-T/Wohnung-Miete/Berlin/Berlin/Prenzlauer-Berg-Prenzlauer-Berg/3,00-/50,00-/EURO--2500,00?enteredFrom=one_step_search']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        results = response.css('a.result-list-entry__brand-title-container::attr(href)').extract()
        for result in results:
            #print('https://www.immobilienscout24.de'+result)
            yield scrapy.Request(
                        url='https://www.immobilienscout24.de'+result,
                        callback=self.parse_immoresult,
                        cb_kwargs=dict(page_url=result))

        next_page = response.css('a[data-nav-next-page="true"]::attr(href)').extract_first()
        if next_page is not None:
            yield scrapy.Request(
                        url='https://www.immobilienscout24.de'+next_page,
                        callback=self.parse)
        '''with open('immotest.txt', 'wb') as f:
            f.write(response.body)

        self.log('Saved file!')'''

    def parse_immoresult(self, response, page_url):
        page_url = page_url[8:]
        date = datetime.datetime.now().strftime('%Y%m%d')
        filename = 'results/immoscout_'+page_url+'_'+date+'.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
