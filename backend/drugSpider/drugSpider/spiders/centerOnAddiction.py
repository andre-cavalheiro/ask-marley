import scrapy
from scrapy.xlib.pydispatch import dispatcher
import pickle
import os
import re
from config import outputs

# Run: scrapy crawl drugSpider -> Must be run inside the FIRST drugSpider dir in order to output to the right place
# Check pickle files:  python -mpickle .\output\centerOnAddiction\drugSymptomsPerType.pkl

class BlogSpider(scrapy.Spider):
    name = 'drugSpider2'
    failedUrls = []
    sucessCases = []
    start_urls = ["https://www.centeronaddiction.org/addiction/commonly-used-illegal-drugs"]

    def __init__(self):
        dispatcher.connect(self.spider_closed, scrapy.signals.spider_closed)

    # Fixme - still work to be done
    def parse(self, response):

        drugTypes = []
        drugEffects = []

        # Extract drug types
        types = response.css('.field-collection-item-field-drug-table')
        for t in types:
            drugTypes.append(t.css('span::text').get().lower())

        # Extract effects of given types
        effects = response.css('.field-items')
        for it, e in enumerate(effects):
            if it < 3 or it > 9:
                continue
            drugEffects.append(e.css('p::text').getall())

        # print(len(drugTypes))
        # print(len(drugEffects))
        assert(len(drugTypes) == len(drugEffects))

        # Associate to each type its symptoms and risks
        keys = ["Acute Effects:", "Health Risks:"]
        labels = ["effects", "risks"]
        keyIndex = 0
        effectsByDrug = {type: {"effects": '', "risks": ''} for type in drugTypes}

        # By the end of this loop the "effects" and "risks" of effectsByDrug will be arrays of strings and not strings
        for it, type in enumerate(drugTypes):
            for it2, phrase in enumerate(drugEffects[it]):
                if effectsByDrug[type][labels[keyIndex]] == '':
                    effectsByDrug[type][labels[keyIndex]] = phrase
                else:
                    effectsByDrug[type][labels[keyIndex]] += ';'
                    effectsByDrug[type][labels[keyIndex]] += phrase

                if keyIndex != len(keys) - 1 and it2 != len(drugEffects[it]) - 1:
                    if keys[keyIndex + 1] in drugEffects[it][it2 + 1]:
                        # Process acquired data
                        effectsByDrug[type][labels[keyIndex]] = re.sub(keys[keyIndex], '', \
                                                                     effectsByDrug[type][labels[keyIndex]]).split(';')
                        for it3, s in enumerate(effectsByDrug[type][labels[keyIndex]]):
                            effectsByDrug[type][labels[keyIndex]][it3] = s.lower().strip()

                        # Increment key / label index
                        keyIndex += 1

            # Process acquired data for the last label
            effectsByDrug[type][labels[keyIndex]] = re.sub(keys[keyIndex], '', \
                                                         effectsByDrug[type][labels[keyIndex]]).split(';')
            for it3, s in enumerate(effectsByDrug[type][labels[keyIndex]]):
                effectsByDrug[type][labels[keyIndex]][it3] = s.lower().strip()

            keyIndex = 0

        print(">>>>> IGNORING OTHER COMPOUNDS FOR NOW <<<<<<<")
        del effectsByDrug["other compounds"]
        print(">>>>> Still have to fix CLUB DRUGS - arrays are empty <<<<<")

        # Save content in files for further analysis
        filename = os.path.join(outputs['centerOnAddiction'], outputs['drugTypes'])
        with open(filename, 'wb') as f:
            pickle.dump(drugTypes, f)

        filename = os.path.join(outputs['centerOnAddiction'], outputs['drugSymptomsPerType'])
        with open(filename, 'wb') as f:
            pickle.dump(effectsByDrug, f)

    def spider_closed(self, spider):
        pass
