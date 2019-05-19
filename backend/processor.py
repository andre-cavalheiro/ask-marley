from utils import *

# File to process and respond to each query

class DrugProcessor:

    drugIdToInfo = []       # Index by drug ID
    drugIdToEffectsId = []  # Index by drug ID

    effectIdToName = []     # Indexed by effects ID
    effectIdToDrugId = []   # Indexed by effects ID

    drugDictionary = {}     # Indexed by drug Name
    effectDictionary = {}   # Indexed by effect Name

    def __init__(self):
        # Import data
        # fixme - Dummy values
        self.drugIdToInfo = [{"name": "Marijuana", "info": "Gets you high as fuck"},
                             {"name": "Heroin", "info": "Gets your life all as fuck"},
                             {"name": "Alcohol", "info": "Makes your head hurt the next day"},
                             {"name": "LSD", "info": "Changes your life"}
                             ]
        self.effectIdToName = ["high", "sick", "headache", "scratching", "light headed", "Hallucinating"]
        self.drugIdToEffectsId = [[0, 4], [1, 3], [1, 2], [0, 4, 5]]
        self.effectIdToDrugId = buildReverseArrayOfArrays(len(self.effectIdToName), self.drugIdToEffectsId)

        self.drugDictionary = {info["name"]: id for id, info in enumerate(self.drugIdToInfo)}
        self.effectDictionary = {name: id for id, name in enumerate(self.effectIdToName)}

    def processQuery(self, searchTerm):
        # fixme - Transform searchTerm into list of Effects
        # fixme - Dummy values
        listOfEffects = ["high", "sick", "light headed"]
        listOfEffectIds = convertNamesToId(self.effectDictionary, listOfEffects)
        matchedDrugsPerEffectId = [self.effectIdToDrugId[effectId].copy() for effectId in listOfEffectIds]
        possibleDrugs = intersectionBetweenLists(matchedDrugsPerEffectId)   # [{drugId, numSymptomsMatched}]
        response = respondQuery(self.drugIdToInfo, possibleDrugs, keys=["name", "info"])
        print(response)
        return response

"""
p = DrugProcessor()
p.processQuery()
"""