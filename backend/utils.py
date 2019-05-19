import collections


def buildReverseArrayOfArrays(amountOfEffects, drugIdToEffectsId):
    effectIdToDrugId = [[] for it in range(amountOfEffects)]

    for drugId, effectIdList in enumerate(drugIdToEffectsId):
        for effectId in effectIdList:
            effectIdToDrugId[effectId].append(drugId)

    return effectIdToDrugId


def convertNamesToId(dictionary, arrayToConvert):
    newArray = []
    for name in arrayToConvert:
        newArray.append(dictionary[name])
    return newArray


def intersectionBetweenLists(listOfLists):
    flatList = listOfLists[0]
    for it in range(1, len(listOfLists)):
        flatList += listOfLists[it]

    frequencies = collections.Counter(flatList)
    frequenciesInArray = []
    for key, freq in frequencies.items():
        frequenciesInArray.append({
            "drugId": key,
            "numSymptomsMatched": freq
        })
    frequenciesInArray = sorted(frequenciesInArray, key=lambda x: x["numSymptomsMatched"], reverse=True)
    return frequenciesInArray


def respondQuery(info, possibleDrugs, keys):
    # possibleDrugs -> # [{drugId, numSymptomsMatched}]
    response = []
    # Todo - Apply some sort of threshold here
    print("Applying dummy threshold of one")
    possibleDrugsAfterTreshold = []
    for drug in possibleDrugs:
        if drug['numSymptomsMatched'] > 1:
            possibleDrugsAfterTreshold.append(drug)

    for drug in possibleDrugsAfterTreshold:
        aux = {}
        for k in keys:
            aux[k] = info[drug["drugId"]][k]
        aux["numSymptomsMatched"] = drug["numSymptomsMatched"]
        response.append(aux)
    return response
