dbName = 'drugDB'

# Several symptom labels can have the same ID
singleSymptomNameArq = {
    "label":
    "ID"
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
        "description": "",
        "otherNames": [],
        "types": [],
        "risks": [],
        "symptomsID": [],
        "linksForMoreInfo": []
    }


# Not being used anywhere, just for human analysis
collections = ['drugNameToID', 'drugIDToInfo', 'symptomNameToID', 'symptomIDToInfo']

ilitDrugsInitSeed = [
    {
        "name": "Marijuana",
        "type": "Cannabinoids",
    },
    {
        "name": "Hashish",
        "type": "Cannabinoids",
    },
    {
        "name": "Heroin",
        "type": "Opioids",
    },
    {
        "name": "Opium",
        "type": "Opioids",
    },
    {
        "name": "Cocaine",
        "type": "Stimulants",
    },
    {
        "name": "Amphetamine",
        "type": "Stimulants",
    },

    {
        "name": "Methamphetamine",
        "type": "Stimulants",
    },
    {
        "name": "MDMA",
        "type": "Club Drugs",
    },
    {
        "name": "Flunitrazepam",
        "type": "Club Drugs",
    },
    {
        "name": "Ketamine",
        "type": "Dissociative Drugs",
    },
    {
        "name": "PCP",
        "type": "Dissociative Drugs",
    },
    {
        "name": "Salvia",
        "type": "Dissociative Drugs",
    },
    {
        "name": "Dextromethorphan",
        "type": "Dissociative Drugs",
    },
    {
        "name": "LSD",
        "type": "Hallucinogens",
    },

    {
        "name": "Mescaline",
        "type": "Hallucinogens",
    },
    {
        "name": "Psilocybin",
        "type": "Hallucinogens",
    },
    {
        "name": "Mescaline",
        "type": "Hallucinogens",
    },
    {
        "name": "steroids",
        "type": "Other Compounds",  # fixme
    },
    {
        "name": "Inhalants",
        "type": "Other Compounds",  # fixme
    }
]

