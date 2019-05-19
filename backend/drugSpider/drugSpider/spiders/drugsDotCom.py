import scrapy
from scrapy.xlib.pydispatch import dispatcher
import os,  sys, pickle
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from config import outputs
from dbConfig import ilitDrugsInitSeed

# Run spider: scrapy crawl drugSpider
# Check pickle files:  python -mpickle .\output\drugsDotCom\Marijuana.pkl

class BlogSpider(scrapy.Spider):
    name = 'drugSpider1'
    failedUrls = []
    sucessCases = []

    def __init__(self):
        dispatcher.connect(self.spider_closed, scrapy.signals.spider_closed)

    def start_requests(self):
        baseUrl = 'https://www.drugs.com/illicit'

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
        allUrls = []
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
        else:
            self.sucessCases.append(response.url)

        sectionTitles = ["Introduction"]

        # Get section titles
        for title in response.css('.contentBox')[1].css('h2::text'):
            sectionTitles.append(title.get())

        # Find the location of the titles and the respective content in the corpus
        contents = response.css('.contentBox')[1].css('::text')
        titleIterator = 1
        titleIndexes = [0]

        for it, text in enumerate(contents):
            if text.get() == sectionTitles[titleIterator]:
                titleIndexes.append(it)
                titleIterator += 1
            if titleIterator >= len(sectionTitles):
                break

        # Extract content with the respective title
        sectionContent = [{"title": title, "content": []} for title in sectionTitles]
        sectionIterator = 0

        if len(titleIndexes) is not 0:
            for it, text in enumerate(contents):

                if it not in titleIndexes:
                    sectionContent[sectionIterator]['content'].append(text.get())

                if sectionIterator+1 < len(titleIndexes) and it+1 == titleIndexes[sectionIterator+1]:
                    sectionIterator += 1

            # Save content in files for further analysis
            filename = os.path.join(outputs['DrugsDotCom'], response.meta['currentDrug'] + ".pkl")
            with open(filename, 'wb') as f:
                pickle.dump(sectionContent, f)

            print(">>> Finished {} <<<".format(response.meta['currentDrug']))

    def spider_closed(self, spider):
        print(">>> Finished Execution outputing failed URLs")
        filename = os.path.join(outputs['DrugsDotCom'], outputs['failedURLsName'])
        with open(filename, 'wb') as f:
            pickle.dump(self.failedUrls, f)
        filename = os.path.join(outputs['DrugsDotCom'], outputs['successURLsName'])
        with open(filename, 'wb') as f:
            pickle.dump(self.sucessCases, f)
