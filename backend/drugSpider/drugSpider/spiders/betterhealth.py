import scrapy
from scrapy.xlib.pydispatch import dispatcher
import pickle
import os
import re
from config import outputs

# Run: scrapy crawl drugSpider -> Must be run inside the FIRST drugSpider dir in order to output to the right place
# Check pickle files:  python -mpickle .\output\centerOnAddiction\drugSymptomsPerType.pkl


class BlogSpider(scrapy.Spider):
    name = 'drugSpider3'
    failedUrls = []
    sucessCases = []
    start_urls = ["https://www.betterhealth.vic.gov.au/health/HealthyLiving/How-drugs-affect-your-body"]

    def __init__(self):
        dispatcher.connect(self.spider_closed, scrapy.signals.spider_closed)

    def parse(self, response):
        drugNames = response.css('#phbody_1_phcontentbody_2_pnl>h3::text').getall()
        drugEffects = response.css('#phbody_1_phcontentbody_2_pnl>ul')
        del drugEffects[0:4]
        del drugEffects[6:8]
        assert(len(drugNames)== len(drugEffects))

        drugNamesTreated = []
        effectsPerName = {}
        for it, dt in enumerate(drugNames):
            tt = dt.replace("(", ",").replace(")", "").replace(":", "")
            drugs = tt.split(",")
            drugs = [x.lower().strip() for x in drugs]
            # print(drugs)
            drugNamesTreated.append(drugs[0])
            effects = drugEffects[it].css('li::text').getall()
            effectsPerName[drugs[0]] = {
                 "otherNames": drugs[1:],
                 "symptoms": [ef.replace('\xa0', '').lower() for ef in effects]
            }
            
        # print(effectsPerName)
        # Save content in files for further analysis
        filename = os.path.join(outputs['betterHealth'], outputs['drugNames'])
        with open(filename, 'wb') as f:
            pickle.dump(drugNamesTreated, f)

        filename = os.path.join(outputs['betterHealth'], outputs['drugSymptomsPerDrug'])
        with open(filename, 'wb') as f:
            pickle.dump(effectsPerName, f)

    def spider_closed(self, spider):
        pass
