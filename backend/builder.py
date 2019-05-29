import os
from pymongo import MongoClient
from drugSpider.config import outputs
from dbConfig import dbName, collections, ilitDrugsInitSeed, singleDrugArq, singleSymptomArq, singleSymptomNameArq, singleDrugNameArq
from random import randint
import pickle
import copy
from dbInteractions import *
import json

# File to transform craweled data into a usable state
# C:\Program Files\MongoDB\Server\4.0\bin

# fixme -> Must insert only if there's not an instance in the DB

class builder:

    def __init__(self, startFromScratch=False, loadFromFiles=False):
        client = MongoClient()
        self.db = client[dbName]
        """self.collections = {}
        self.collections['drugNameToID'] = self.db['drugNameToID']
        self.collections['drugIDToInfo'] = self.db['drugIDToInfo']
        self.collections['symptomNameToID'] = self.db['symptomNameToID']
        self.collections['symptomIDToInfo'] = self.db['symptomIDToInfo']
        """


        if not startFromScratch:

            if loadFromFiles:
                print(">> DROPPING CURRENT DATABASE AND LOADING FROM FILES <<")
                self.saveDatabase('dbDumpsOld')
                client.drop_database(dbName)
                self.loadDatabaseFromFile()

            elif not loadFromFiles:
                """
                 Verify if database is empty to inform the user (the previous declarations will not influence
                 the following code since mongo only creates the collections once an item is inserted.
                """
                print(">> USING DATABASE AS IS <<")
                emptyCollections = []
                for c in collections:
                    if c in self.db.list_collection_names():
                        if self.db[c].count() == 0:
                            emptyCollections.append(c)
                    else:
                        emptyCollections.append(c)

                if len(emptyCollections) is not 0:
                    print("> WARNING <")
                    print(">> The database did not have the following collections filled")
                    print(emptyCollections)

        if startFromScratch:
            print(">>> DROPPING DATABASE <<<")
            self.saveDatabase('dbDumpsOld')
            client.drop_database(dbName)
            self.initDB()

    def initDB(self):
        # Initiate database based only on the initial seed in dbConfig
        """
        Initiated Collections:
            - drugNameToID
            - drugIDToInfo  with ["ID", "commonName", "types"]
        """
        print("> Initiating collections with seeding data")
        for drug in ilitDrugsInitSeed:
            insertNewDrug(drug['name'], drug['type'])

    def getNewID(self):
        n = 10
        range_start = 10 ** (n - 1)
        range_end = (10 ** n) - 1
        return randint(range_start, range_end)

    def centerOnAddiction(self):
        """
        # fixme - Assumes the info from centerOnAddiction.com is the optimal one (defining as commonName)
        # fixme - Still Not using drug risks
        Uses Collections:
            - symptomNameToID with ["ID", "label"]
            - symptomIDToInfo  with ["ID", "commonName"]
        """
        print("> [Center of Addiction]")

        dir = os.path.join(os.path.join('drugSpider', 'output'), 'centerOnAddiction')

        f1 = open(os.path.join(dir, outputs['drugTypes']), 'rb')
        f2 = open(os.path.join(dir, outputs['drugSymptomsPerType']), 'rb')

        types = pickle.load(f1)
        effectsPerDrug = pickle.load(f2)

        for type in types:
            # First insert the symptoms in the symptom name to ID collection:
            if type != 'other compounds':
                addDataToDrugTypes(type, "symptomName", 'symptomsID', effectsPerDrug[type]['effects'])
                addDataToDrugTypes(type, "raw", 'risks', effectsPerDrug[type]['risks'])

                """
                for effect in effectsPerDrug[type]['effects']:
                    if effect is not '':
                        id = getSymptomOrCreate(effect)
                        '''
                        s = copy.deepcopy(singleSymptomNameArq)
                        s["label"] = effect.lower()
                        s["ID"] = self.getNewID()
                        self.collections['symptomNameToID'].insert_one(s)

                        s_ = copy.deepcopy(singleSymptomArq)
                        s_["commonName"] = s["label"]
                        s_["ID"] = s["ID"]
                        self.collections['symptomIDToInfo'].insert_one(s_)
                        '''

                        # Then insert the very same ID in the effects associated with the drugs of the given type
                        for drug in self.collections['drugIDToInfo'].find({"types": type}):
                            self.collections['drugIDToInfo'].update_one(
                                {
                                    '_id': drug['_id'],
                                }, {
                                    '$set': {
                                        'symptomsID': drug['symptomsID'] + [s["ID"]]
                                    }
                                 }, upsert=False)
                """
            else:
                print("IGNORING OTHER COMPOUNDS")

    def betterHealth(self):
        """
        Uses Collections:
            - symptomNameToID with ["ID", "label"]
            - symptomIDToInfo  with ["ID", "commonName"] 
        """
        print("> [Better Health]")

        dir = os.path.join(os.path.join('drugSpider', 'output'), 'betterHealth')

        f1 = open(os.path.join(dir, outputs['drugNames']), 'rb')
        f2 = open(os.path.join(dir, outputs['drugSymptomsPerDrug']), 'rb')

        drugNames = pickle.load(f1)
        effectsPerDrug = pickle.load(f2)

        for drug in drugNames:
            drugID = getDrugIDOrCreate(drug, effectsPerDrug[drug]['otherNames'], "")     # fixme - having the risk of inserting empty type
            appendDataToDataFieldInSingleDrug("ID", drugID, "otherNames", effectsPerDrug[drug]['otherNames'])
            appendSymptoms("ID", drugID, "names", effectsPerDrug[drug]['symptoms'])
            """
            # Find if drug already exists
            print(drug)
            numResults = self.collections['drugIDToInfo'].count_documents(({"commonName": drug}))
            numResultsSynonyms = self.collections['drugIDToInfo'].count_documents({"otherNames": drug})

            if numResults == 0 and numResultsSynonyms == 0:
                #Create new drug entry
                print("Creating new drug - pass")
                pass
            elif numResultsSynonyms == 0:
                # Append other names to existing drug
                print("Append other names to existing drug (Synonym)")
                self.collections['drugIDToInfo'].find_and_modify(
                    query={"commonName": drug},
                    update={
                        '$push':
                            {
                                "otherNames": { '$each':
                                                    effectsPerDrug[drug]['otherNames']
                                                }
                            }
                    })

                symptomIDs = []
                for symptom in effectsPerDrug[drug]['symptoms']:
                    symptomID = None
                    # Check if symptom exists if not create it
                    numSymptomsMatches = self.collections['symptomNameToID'].count_documents({"label": symptom})
                    if numSymptomsMatches == 0:
                        # Create new symptom
                        print("Creating Symptom")
                        s = copy.deepcopy(singleSymptomNameArq)
                        s["label"] = symptom
                        s["ID"] = self.getNewID()
                        self.collections['symptomNameToID'].insert_one(s)
                        symptomID = s["ID"]
                    else:
                        # Adding existing symptom
                        print("Adding existing symptom")
                        dbInstance = self.collections['symptomNameToID'].find_one({"label": symptom}, {'ID': 1, '_id': 0})
                        symptomID = dbInstance['ID']
                        print(symptomID)
                    symptomIDs.append(symptomID)
                print(symptomIDs)
                # Insert symptoms
                self.collections['drugIDToInfo'].find_and_modify(
                    query={"commonName": drug},
                    update={
                        '$push':
                            {
                                "symptomsID": {'$each':
                                                   symptomIDs
                                               }
                            }
                    })

            elif numResults == 0:
                print("Append other names to existing drug (origName) - pass")
                # Append other names
                for otherName in effectsPerDrug["otherNames"]:
                    pass
                # Append symptoms for drug
                for otherName in effectsPerDrug["symptoms"]:
                    pass
            """

    def drugsDotCom(self):
        print("> [Drugs.Com]")

        dir = os.path.join(os.path.join('drugSpider', 'output'), 'DrugsDotCom')
        f1 = open(os.path.join(dir, outputs['crawledDrugs']), 'rb')
        drugNames = pickle.load(f1)

        for drugName in drugNames:
            f1 = open(os.path.join(dir, drugName + '.pkl'), 'rb')
            drugData = pickle.load(f1)
            drugID = getDrugIDOrCreate(drugName, [], "")     # fixme - having the risk of inserting empty type
            for dataField in drugData.keys():
                appendDataToDataFieldInSingleDrug("ID", drugID, dataField, [drugData[dataField]])

    def saveDatabase(self, dir):
        for col in collections:
            self.saveCollection(col, dir)

    def saveCollection(self, collectionName, dir):
        col = self.db[collectionName]

        cursor = col.find({}, {'_id': False})
        file = open(os.path.join(dir, collectionName + ".json"), "w")
        file.write('[')
        for document in cursor:
            file.write(json.dumps(document))
            file.write(',')
        file.write(']')

    def loadDatabaseFromFile(self):
        pass

deleteAndReboot = False
loadFromFile = False
a = builder(startFromScratch=deleteAndReboot, loadFromFiles=loadFromFile)
if deleteAndReboot:
    a.centerOnAddiction()
    a.betterHealth()
    a.drugsDotCom()
a.saveDatabase('dbDumps')