from billy.scrape.expenditures import TransactionalExpenditureScraper, AggregatedExpenditureScraper, TransactionalExpenditure, AggregatedExpenditure
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

            fiscal_year = None
            amount = None
            recipient_name = None
            spending_type = None
    
            if sheet.cell_value(row_num, 1) and sheet.cell_value(row_num, 3) and sheet.cell_value(row_num, 4) and sheet.cell_value(row_num, 6) :
                fiscal_year = sheet.cell_value(row_num, 3)
                amount = float(sheet.cell_value(row_num, 4)) 
                recipient_name = sheet.cell_value(row_num, 1)
                spending_type = sheet.cell_value(row_num, 6).lower()
            else:
                continue

            record = {}
            if sheet.cell_value(row_num, 0):
                record['agency_name'], record['subagency_name'] = self.split_agency(sheet.cell_value(row_num, 0))
            if sheet.cell_value(row_num, 2):
                record['recipient_zip'] = sheet.cell_value(row_num, 2)
            if sheet.cell_value(row_num, 5):
                record['description'] = sheet.cell_value(row_num, 5)

#            print record
            exp = TransactionalExpenditure(fiscal_year, spending_type, recipient_name, amount, **record)
            exp.add_source(url)
            self.save_object(exp)

    def scrape_payments(self):
        url = 'http://spending.dbm.maryland.gov/'
        

    def scrape(self, fiscal_year):   

        self.scrape_grants()
        self.scrape_payments()




