from billy.scrape.expenditures import TransactionalExpenditureScraper, AggregatedExpenditureScraper
from collections import defaultdict
import lxml.html
import xlrd
from urllib import quote
import pprint
BASE_URL = 'http://datapoint.apa.virginia.gov/exp/exp_mobj.cfm'
# scraper returns urls relative to this
TOP_URL = 'http://datapoint.apa.virginia.gov/exp/'
# we only care about object, as everything is accessible from everything else
# final URL looks like
# http://datapoint.apa.virginia.gov/exp/exp_mobj_obj_agy_voucher.cfm?&ShowAll=Yes&AGY=109&OBJ=426&FY=2013
# top-level:
    # object
        # 'major object' //td[@class="DataA"]/a and //td[@class="DataB"]/a
            # object //td[@class="DataA"]/div/a
                # program (we can skip this because we just want the table data)
                    # yearly //table[1]/tbody/tr[1]/td (list of th w/ years, [2:] is what we want)
                    # //table[1]/tbody/tr/td[XXX] where XXX is the above index
                    # then follow [1:] and tack on &ShowAll=Yes to the resulting URL
                        # agency, payee, voucher number, transaction date, amt
                        # grab entire table and do it.
                # FIXME save drilldown path?


class VATransactionalExpenditureScraper(TransactionalExpenditureScraper):
    scraper_type = 'transactional_expenditures'
    jurisdiction = 'va'
    links_xpath = {
        'Major Object': '//td[@class="%s"]/a',
        'Object': '//td[@class="%s"]/a',
        'Yearly': '//table[1]/tbody/tr[1]/td',
        'Column': '//table[1]/tbody/tr/td[%s]'
    }
    table_classes = ['DataA', 'DataB']

    def pull_page(self, url):
        html = self.urlopen(url)
        doc = lxml.html.fromstring(html)
        return doc

    # FIXME combine these two, dummy
    def get_statewide(self, url):
        doc = self.pull_page(url)
        parts_a = self.links_xpath['Major Object'] % 'DataA'
        parts_b = self.links_xpath['Major Object'] % 'DataB'
        major_objects_a = doc.xpath(parts_a)
        major_objects_b = doc.xpath(parts_b)
        all_objs = major_objects_b + major_objects_a
        top_links = []
        for ele in all_objs:
            top_links.append(TOP_URL + ele.get('href').replace(' ', '%20'))
        return top_links

    def get_statewide_objects(self, url):
        doc = self.pull_page(url)
        parts_a = self.links_xpath['Object'] % 'DataA'
        parts_b = self.links_xpath['Object'] % 'DataB'
        major_objects_a = doc.xpath(parts_a)
        major_objects_b = doc.xpath(parts_b)
        all_objs = major_objects_b + major_objects_a
        top_links = []
        for ele in all_objs:
            top_links.append(TOP_URL + ele.get('href').replace(' ', '%20'))
        return top_links

    def get_yearly(self, url):
        ''' get the last list of stuff
            here we have our list of objects and agencies and FY
        '''
        doc = self.pull_page(url)
        agency_ids = []
        yearly_links = doc.xpath(self.links_xpath['Yearly'])[2:]
        for yeal in yearly_links:
            agency_ids.append(TOP_URL + yeal.get('href').replace(' ', '%20'))
        return agency_ids

    def scrape(self, url):
        # get the top-level
        top_level = self.get_statewide(BASE_URL)
        statewide_objs = []
        for subobj in top_level:
            stateobj = self.get_statewide_objects(subobj)
            for so in stateobj:
                yl = self.get_yearly(so)
            
