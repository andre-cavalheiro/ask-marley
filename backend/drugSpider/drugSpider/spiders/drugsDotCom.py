import scrapy
from scrapy.xlib.pydispatch import dispatcher
import os,  sys, pickle
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from config import outputs
from dbConfig import ilitDrugsInitSeed, titleConverter

# Run spider: scrapy crawl drugSpider
# Check pickle files:  python -mpickle .\output\drugsDotCom\Marijuana.pkl

class BlogSpider(scrapy.Spider):
    name = 'drugSpider1'
    failedUrls = []
    crawledDrugs = []

    def __init__(self):
        dispatcher.connect(self.spider_closed, scrapy.signals.spider_closed)

    def start_requests(self):
        baseUrl = 'https://www.drugs.com/illicit'
        allUrls = []

        # Dummy
        """
        ilicitDrugLegitNames = [
            {
                "name": "Marijuana",
                "ID": int()
            },
            {
                "name": "MDMA",
                "ID": int()
            },
        ]
        """
        # Build URLS searching for specific drugs
        # for drug in ilicitDrugLegitNames:
        #    allUrls.append('{}/{}.html'.format(baseUrl, drug['name']))


        for drug in ilitDrugsInitSeed:
            allUrls.append('{}/{}.html'.format(baseUrl, drug['name']))

        print(">>> About to evaluate {} URLs".format(len(allUrls)))

        for it, url in enumerate(allUrls):
            yield scrapy.Request(url=url, callback=self.parse,
                                 meta={
                                     "currentDrug": ilitDrugsInitSeed[it]["name"],
                                 })

    def parse(self, response):

        if response.status is not 200:
            # Had to allow 404 in the settings file
            print(">>> Status for {} was {} <<<".format(response.meta['currentDrug'], response.status))
            self.failedUrls.append(response.url)
            return

        sectionTitles = ["Introduction"]

        # Get section titles
        for title in response.css('.contentBox')[1].css('h2::text'):
            sectionTitles.append(title.get().lower())

        # Find the location of the titles and the respective content in the corpus
        contents = response.css('.contentBox')[1].css('::text')
        titleIterator = 1
        titleIndexes = [0]

        for it, text in enumerate(contents):
            if text.get().lower() == sectionTitles[titleIterator]:
                titleIndexes.append(it)
                titleIterator += 1
            if titleIterator >= len(sectionTitles):
                break

        # Extract content with the respective title
        sectionContent = [{"title": title.lower(), "content": []} for title in sectionTitles]
        sectionIterator = 0

        for it, text in enumerate(contents):

            if it not in titleIndexes:
                sectionContent[sectionIterator]['content'].append(text.get())

            if sectionIterator+1 < len(titleIndexes) and it+1 == titleIndexes[sectionIterator+1]:
                sectionIterator += 1

        # Convert information to usable state
        drugData = {}
        for section in sectionContent:
            # todo - ONLY FOR DEBUGGING
            f = False
            if response.meta['currentDrug'].lower() == "cocaine":
                """print(section["title"])
                print('---')
                print(datakey)"""
                f = True

            datakey = self.retrieveSectionIdentifier(section["title"], f)

            if datakey is not None:
                print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>PASSED " + datakey)
                drugData[datakey] = ''
                for data in section["content"]:
                    drugData[datakey] += data.lower().replace('\r\n', '').replace('\n', '')

                drugData[datakey] = drugData[datakey]
        print(drugData)

        # Save content in files for further analysis
        filename = os.path.join(outputs['DrugsDotCom'], response.meta['currentDrug'] + ".pkl")
        with open(filename, 'wb') as f:
            pickle.dump(drugData, f)

        self.crawledDrugs.append(response.meta['currentDrug'].lower())
        print(">>> Finished {} <<<".format(response.meta['currentDrug']))


    def retrieveSectionIdentifier(self, sectionName, f=False):
        """converter__ = {
            'what is': '',
            'important information': '',
            'effects': '',
            'health hazards': '',
            'pregnancy': '',
            'extent': '',
            'recreational use': '',
            'side effects': '',
            'abuse': '',
        }"""

        for infoSec in titleConverter.keys():
            for possibleSecTitles in titleConverter[infoSec]:
                if f:
                    pass
                    # print(sectionName.lower())
                    # print("---")
                    # print(possibleSecTitles)
                if possibleSecTitles in sectionName.lower():
                    #print("DING DING DING")
                    return infoSec
        return None

    def spider_closed(self, spider):
        print(">>> Finished Execution outputing failed URLs")
        filename = os.path.join(outputs['DrugsDotCom'], outputs['failedURLsName'])
        with open(filename, 'wb') as f:
            pickle.dump(self.failedUrls, f)
        filename = os.path.join(outputs['DrugsDotCom'], outputs['crawledDrugs'])
        with open(filename, 'wb') as f:
            pickle.dump(self.crawledDrugs, f)
