from billy.scrape.expenditures import TransactionalExpenditureScraper


class Scraper(TransactionalExpenditureScraper):
    scraper_type = 'transactional_expenditures'
    jurisdiction = 'ny'

    def scrape(self, *args, **kwargs):
        worst_url_ever = ('http://wwe1.osc.state.ny.us/transparency/contracts/'
               'contractresults.cfm?DocType=xls&sb=a&a=Z0000&ac=&v=%28'
               'Enter+Vendor+Name%29&vo=B&cn=&c=-1&m1=0&y1=0&m2=0&y2=0&am'
               '=0&b=Search&order=VENDOR_NAME&sort=ASC'
        import pdb; pdb.set_trace()
