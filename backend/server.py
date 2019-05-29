import falcon
from falcon_cors import CORS
from processor import DrugProcessor
from pymongo import MongoClient
import dbInteractions
import json

# waitress-serve --port=8000 server:api

cors = CORS(allow_all_origins=True,
                      allow_all_headers=True,
                      allow_all_methods=True)

api = falcon.API(middleware=[cors.middleware])

api.req_options.auto_parse_form_urlencoded=True

class search:
    def on_post(self,    req, resp):
        print(req.media)
        posted_data = req.media
        searchType = posted_data["searchType"]

        payload = []
        if searchType=="query":
            searchTerm = posted_data['searchTerm']
            print("Searched for {}".format(searchTerm))
            '''payload = [
                {
                    'name': "Marijuana",
                    'effects': 'Getting high as fuck',
                    'moreInfo': 'www.snoopDogg.com'
                },
                {
                    'name': "Heroin",
                    'effects': 'Getting your life fucked',
                    'moreInfo': 'www.howToFuckUpMyLife.com'
                }
            ]'''
            payload = processor.processQuery(searchTerm)  # fixme

        elif searchType == "checkBox":
            symptoms = posted_data["symptoms"]
            possibleDrugs = {}
            print("Matches:")
            for id in symptoms:
                for drug in drugIDToInfo.find({"symptomsID": id}):
                    print(drug['ID'])
                    drug.pop('_id')
                    if drug['ID'] not in possibleDrugs.keys():
                        drug['symptomsMatched'] = 1
                        possibleDrugs[drug['ID']] = drug
                    else:
                        possibleDrugs[drug['ID']]['symptomsMatched'] += 1

            print("Applying treshold")
            matchedResults = []
            for id in possibleDrugs.keys():
                matchedResults.append(possibleDrugs[id]['symptomsMatched'])
            s = list(sorted(set(matchedResults), reverse=True))
            idsToDel = []
            print(s)
            if len(s)>2:
                for id in possibleDrugs.keys():
                    if possibleDrugs[id]['symptomsMatched'] <= s[-2]:
                        idsToDel.append(id)
                for id in idsToDel:
                    del possibleDrugs[id]

            elif len(s)==2:
                for id in possibleDrugs.keys():
                    if possibleDrugs[id]['symptomsMatched'] <= s[-1]:
                        idsToDel.append(id)
                for id in idsToDel:
                    del possibleDrugs[id]

            elif len(s)==1:
                pass

            else:
                possibleDrugs = {}

            payload = possibleDrugs

        resp.media = payload

class getDrugs:
    def on_post(self, req, resp):
        print(req.media)
        posted_data = req.media

        getAllDrugs = bool(posted_data['getAllDrugs'])

        payload = []

        if getAllDrugs == True:
            for drug in drugIDToInfo.find({}):
                drug.pop('_id')
                payload.append(drug)
        else:
            fetchingMethod = posted_data['fetchingMethod']
            drugs = posted_data['drugs']

            if fetchingMethod == "ID":
                for id in drugs:
                    drug = drugIDToInfo.find_one({"ID": id})
                    drug.pop('_id')
                    payload.append(drug)

            elif fetchingMethod == "type":
                for type in drugs:
                    for drug in drugIDToInfo.find({"types": type}):
                        drug.pop('_id')
                        payload.append(drug)

            elif fetchingMethod == "name":
                for name in drugs:
                    drug = drugNameToID.find_one({"name": name})
                    drug = drugIDToInfo.find_one({"ID": drug["ID"]})
                    drug.pop('_id')
                    payload.append(drug)

        resp.media = payload

class getSymptoms:
    def on_post(self, req, resp):
        print(req.media)
        posted_data = req.media
        getAllSymptoms = bool(posted_data['getAllSymptoms'])
        payload = []

        if getAllSymptoms == True:
            for symptom in symptomIDToInfo.find({}):
                symptom.pop('_id')
                payload.append(symptom)
        else:
            fetchingMethod = posted_data['fetchingMethod']
            symptoms = posted_data['symptoms']

            if fetchingMethod == "ID":
                for id in symptoms:
                    symptom = symptomIDToInfo.find_one({"ID": id})
                    symptom.pop('_id')
                    payload.append(symptom)

            elif fetchingMethod == "name":
                for name in symptoms:
                    symptom = symptomNameToID.find_one({"label": name})
                    symptom = symptomIDToInfo.find_one({"ID": symptom["ID"]})
                    symptom.pop('_id')
                    payload.append(symptom)

        print("=== RESP ===")
        print(payload)
        resp.media = payload

class mergeSymptoms:
    def on_post(self, req, resp):
        print(req.media)
        posted_data = req.media
        oldSymptoms = posted_data['oldSymptomIDs']
        newCommonName = posted_data['newCommonName']
        id, n1, n2, n3 = dbInteractions.mergeSymptoms(oldSymptoms, newCommonName)
        worked = False
        workedForAll = False
        print(n2.matched_count)
        print(n3.matched_count)

        if (n2.matched_count==n2.modified_count) and (n3.matched_count==n3.modified_count) and \
                (n2.matched_count==1) and (n3.matched_count==1):
            worked=True

        if n1.matched_count==n1.modified_count:
            workedForAll = True

        payload = {
            'id': id,
            'worked': worked,
            'workedForAll': workedForAll,
            'changedDocs1': n1.modified_count,

        }
        resp.media = payload

processor = DrugProcessor()

client = MongoClient()

db = client["drugDB"]

drugNameToID = db['drugNameToID']
drugIDToInfo = db['drugIDToInfo']

symptomNameToID = db['symptomNameToID']
symptomIDToInfo = db['symptomIDToInfo']

api.add_route('/search', search())
api.add_route('/getDrugs', getDrugs())
api.add_route('/getSymptoms', getSymptoms())
api.add_route('/mergeSymptoms', mergeSymptoms())