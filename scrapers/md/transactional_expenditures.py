from billy.scrape.expenditures import TransactionalExpenditureScraper, AggregatedExpenditureScraper
from collections import defaultdict
import lxml.html
import xlrd


class MDTransactionalExpenditureScraper(TransactionalExpenditureScraper):
    jurisdiction = 'md'
    

    def scrape_grants(self):
        url = 'http://dbm.maryland.gov/agencies/operbudget/Pages/grantspayments.aspx'
        html = self.urlopen(url)
        doc = lxml.html.fromstring(html)
        doc.make_links_absolute(url)
        download_url = doc.xpath("//a[text()='Export All Records']")[0].get('href')
        print download_url

    def scrape_payments(self):
        url = 'http://spending.dbm.maryland.gov/'
        

    def scrape(self, fiscal_year):   

        self.scrape_grants()
        self.scrape_payments()
