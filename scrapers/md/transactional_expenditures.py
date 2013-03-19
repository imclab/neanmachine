from billy.scrape.expenditures import TransactionalExpenditureScraper, AggregatedExpenditureScraper
from collections import defaultdict
import lxml.html
import xlrd
import tempfile
import shutil


class MDTransactionalExpenditureScraper(TransactionalExpenditureScraper):
    jurisdiction = 'md'
    
    def split_agency(self, agency_text):
        return agency_text.split('/', 1)

    def split_value(self, raw_cell):
        return raw_cell.split(':')[1] or None

    def scrape_grants(self):
        url = 'http://dbm.maryland.gov/agencies/operbudget/Pages/grantspayments.aspx'
        html = self.urlopen(url)
        doc = lxml.html.fromstring(html)
        doc.make_links_absolute(url)
        download_url = doc.xpath("//a[text()='Export All Records']")[0].get('href')
        filename, response = self.urlretrieve(download_url)
        sheet = xlrd.open_workbook(filename).sheet_by_index(0)

        for row_num in range(sheet.nrows):
            if row_num == 0:
                continue

            row_data = sheet.row(row_num)

            record = {}
            record['agency_name'], record['subagency_name'] = self.split_agency(sheet.cell_value(row_num, 0))
            record['recipient_name'] = sheet.cell_value(row_num, 1)
            record['recipient_zip'] = sheet.cell_value(row_num, 2)
            record['fiscal_year'] = sheet.cell_value(row_num, 3)
            record['amount'] = float(sheet.cell_value(row_num, 4) or 0) 
            record['description'] = sheet.cell_value(row_num, 5)
            record['spending_type'] = sheet.cell_value(row_num, 6).lower()

            print record
                

    def scrape_payments(self):
        url = 'http://spending.dbm.maryland.gov/'
        

    def scrape(self, fiscal_year):   

        self.scrape_grants()
        self.scrape_payments()
