import os

dirs = {
    'output': 'output'
}

outputs = {
    'DrugsDotCom': os.path.join(dirs['output'], 'drugsDotCom'),
    'centerOnAddiction': os.path.join(dirs['output'], 'centerOnAddiction'),
    'betterHealth': os.path.join(dirs['output'], 'betterHealth'),

    'drugTypes': 'drugTypes.pkl',
    'drugSymptomsPerType': 'drugSymptomsPerType.pkl',
    'drugNames': 'drugNames.pkl',
    'drugSymptomsPerDrug': 'drugSymptomsPerDrug.pkl',
    'failedURLsName': 'failedURLs.pkl',
    'successURLsName': 'successURLs.pkl',
}