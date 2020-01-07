import scrapy

class DividendsSpider(scrapy.Spider):
    name = "dividends"
    start_urls = [
            'http://www.infobolsa.es/mercado-nacional/mercado-continuo'
            ]

    def parse(self, response):
        links = response.xpath('//div[@id="instrumentListTable"]/table/tbody/tr/td/a/@href')
        for link in links:
            if link is not None:
                next_page = response.urljoin(link.extract())
                yield scrapy.Request(next_page, callback=self.parse_company)

    def parse_company(self, response):
        menu = response.xpath('//div[@class="horzMenuSlider"]')
        link = menu.xpath(".//a[contains(@href,'/cotizacion/dividendos')]/@href").extract_first()
        link = link.replace('\n','').replace('\r','').replace(' ','')
        next_page = response.urljoin(link)
        yield scrapy.Request(next_page, callback=self.parse_dividends)


    def parse_dividends(self, response):
        rows = response.xpath('//tbody[@id="historicalDividendsRows"]/tr')
        for row in rows:
            date = row.xpath('.//td[@class="date"]/text()').extract_first()
            exercice = row.xpath('.//td[@class="exercice"]/text()').extract_first()
            concept = row.xpath('.//td[@class="concept"]/@data-value').extract_first()
            amount = row.xpath('.//td[@class="amount"]/text()').extract_first().replace(',','.')
            company = response.url.replace('http://www.infobolsa.es/cotizacion/dividendos-','')
            price = row.xpath('//*[@id="stockSummary"]/div/div[2]/div[1]/div[2]/div[1]/text()').extract_first()
            yield {
                    'company': company,
                    'date': date,
                    'exercice': exercice,
                    'concept': concept,
                    'amount': amount,
                    'price': price
                    }
