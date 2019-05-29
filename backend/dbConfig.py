dbName = 'drugDB'

# Several symptom labels can have the same ID
singleSymptomNameArq = {
    "label": "",
    "ID": int()
}

# Several drug names can have the same ID
singleDrugNameArq = {
    "name": "",
    "ID": int()
}

singleSymptomArq = {
    "ID": int(),
    "commonName": "",
    "description": "",
}

singleDrugArq = {
        "ID": int(),
        "commonName": "",
        "descriptions": "",
        "otherNames": [],
        "types": [],
        "risks": [],
        "symptomsID": [],
        "linksForMoreInfo": []
    }

titleConverter = {
    'description': ['what is'],
}    # 'linksForMoreInfo': ['']


# Not being used anywhere, just for human analysis
collections = ['drugNameToID', 'drugIDToInfo', 'symptomNameToID', 'symptomIDToInfo']

ilitDrugsInitSeed = [
    {
        "name": "marijuana",
        "type": "cannabinoids",
    },
    {
        "name": "hashish",
        "type": "cannabinoids",
    },
    {
        "name": "heroin",
        "type": "opioids",
    },
    {
        "name": "opium",
        "type": "opioids",
    },
    {
        "name": "cocaine",
        "type": "stimulants",
    },
    {
        "name": "amphetamine",
        "type": "stimulants",
    },

    {
        "name": "methamphetamine",
        "type": "stimulants",
    },
    {
        "name": "mdma",
        "type": "club drugs",
    },
    {
        "name": "flunitrazepam",
        "type": "club drugs",
    },
    {
        "name": "ketamine",
        "type": "dissociative drugs",
    },
    {
        "name": "pcp",
        "type": "dissociative drugs",
    },
    {
        "name": "dalvia",
        "type": "dissociative drugs",
    },
    {
        "name": "dextromethorphan",
        "type": "dissociative drugs",
    },
    {
        "name": "lsd",
        "type": "hallucinogens",
    },

    {
        "name": "mescaline",
        "type": "hallucinogens",
    },
    {
        "name": "psilocybin",
        "type": "hallucinogens",
    },
    {
        "name": "mescaline",
        "type": "hallucinogens",
    },
    {
        "name": "steroids",
        "type": "other compounds",  # fixme
    },
    {
        "name": "inhalants",
        "type": "other compounds",  # fixme
    }
]

