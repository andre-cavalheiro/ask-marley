from pymongo import MongoClient
from dbConfig import singleDrugArq, singleSymptomArq, singleSymptomNameArq, singleDrugNameArq, dbName
from random import randint
import copy

client = MongoClient()
db = client[dbName]
drugNameToID = db['drugNameToID']
drugIDToInfo = db['drugIDToInfo']
symptomNameToID = db['symptomNameToID']
symptomIDToInfo = db['symptomIDToInfo']

def insertNewDrug(name, type):
    d = copy.deepcopy(singleDrugArq)
    dN = copy.deepcopy(singleDrugNameArq)
    id = getNewID()

    d["commonName"] = name.lower()
    d["types"].append(type.lower())
    d["ID"] = id

    dN["name"] = name
    dN["ID"] = id

    drugIDToInfo.insert_one(d)
    drugNameToID.insert_one(dN)
    print("New drug [{}] inserted".format(d["commonName"]))
    return id

def insertNewSymptom(symptom):
    # symptom is a string
    s = copy.deepcopy(singleSymptomNameArq)
    s_ = copy.deepcopy(singleSymptomArq)

    id = getNewID()

    s["label"] = symptom.lower()
    s["ID"] = id

    s_["commonName"] = symptom
    s_["ID"] = id

    symptomNameToID.insert_one(s)
    symptomIDToInfo.insert_one(s_)

    print("New symptom [{}] inserted".format(id))
    return id

def getSymptomIDOrCreate(label):
    numResults = symptomIDToInfo.count_documents(({"commonName": label}))
    if numResults == 0:
        return insertNewSymptom(label)
    else:
        d = symptomIDToInfo.find_one({"commonName": label})
        print("Symptom {} found".format(d['ID']))
        return d['ID']

def getDrugIDOrCreate(commonName, otherNames, type):
    # todo - not considering possible multiple matches because of find_one
    possibleNames = [commonName] + otherNames

    for name in possibleNames:
        numResults = drugIDToInfo.count_documents(({"commonName": name}))
        numResultsSynonyms = drugIDToInfo.count_documents({"otherNames": name})

        if numResults == 0 and numResultsSynonyms == 0:
            continue
        elif numResults == 0:
            d = drugIDToInfo.find_one({"otherNames": name})
            return d['ID']
        else:
            # todo - This else may be dangerous
            d = drugIDToInfo.find_one({"commonName": name})
            print("Drug {} found".format(d['commonName']))
            return d['ID']

    return insertNewDrug(commonName, type)

def addDataToDrugTypes(type, insertionType, positionToFill, data):
    # symptomIDs has to be a list
    # insertionType = "symptomName", "raw"
    if insertionType == "raw":
        for drug in drugIDToInfo.find({"types": type}):
            drugIDToInfo.update_one(
                {
                    '_id': drug['_id'],
                }, {
                    '$set': {
                        positionToFill: drug[positionToFill] + data
                    }
                }, upsert=False)
    elif insertionType == "symptomName":
        symptomIDs = [getSymptomIDOrCreate(s) for s in data]

        for drug in drugIDToInfo.find({"types": type}):
            drugIDToInfo.update_one(
                {
                    '_id': drug['_id'],
                }, {
                    '$set': {
                        'symptomsID': drug['symptomsID'] + symptomIDs
                    }
                }, upsert=False)

def appendDataToDataFieldInSingleDrug(drugIdentifier, drug, dataField, data):
    # drugIdentifier "commonName", "ID"
    drugIDToInfo.find_and_modify(
        query={drugIdentifier: drug},
        update={
            '$push':
                {
                    dataField: {'$each': data }
                }
        })

def appendSymptoms(drugIdentifier, drug, symptomsIdentifier, symptoms):
    # symptomsIdentifier = "commonName", "ID"
    if symptomsIdentifier == "ID":
        print("Symptoms inserted into {}".format(drug))
        print(symptoms)

        drugIDToInfo.find_and_modify(
            query={drugIdentifier: drug},
            update={
                '$push':
                    {
                        "otherNames": {'$each':
                                           symptoms
                                       }
                    }
            })
    elif symptomsIdentifier == "name":
        symptomIDs = [getSymptomIDOrCreate(s) for s in symptoms]
        print("Symptoms inserted into {}".format(drug))
        print(symptomIDs)
        drugIDToInfo.find_and_modify(
            query={drugIdentifier: drug},
            update={
                '$push':
                    {
                        "otherNames": {'$each':
                                           symptomIDs
                                       }
                    }
            })

def mergeSymptoms(oldSymptomsIDs, newCommonName):
    newSymptomID = getNewID()
    print(newSymptomID)
    for id in oldSymptomsIDs:
        # Substitute symptom Ids in drug Info
        r1 = drugIDToInfo.update_many({"symptomsID": id}, {'$set': {'symptomsID.$': newSymptomID}})
        # Substitute symptom IDs in name=>ID mapping
        r2 = symptomNameToID.update_many({"ID": id}, {'$set': {'ID': newSymptomID}})
        # Substitute symptom ID in ID=> Info mapping
        r3 = symptomIDToInfo.update_many({"ID": id}, {'$set': {'ID': newSymptomID, 'commonName': newCommonName}})

    """
    print(r1.modified_count)
    print(r2.matched_count)
    print(r3.acknowledged)
    """
    return newSymptomID,r1,r2,r3


def getNewID():
        n = 10
        range_start = 10 ** (n - 1)
        range_end = (10 ** n) - 1
        return randint(range_start, range_end)