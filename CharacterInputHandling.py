import csv
from project_rio_lib.lookup import Lookup, LookupDicts

charNameDict = {}
char_name_list = []

char_lookup = Lookup().lookup

with open('CharNames.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        char_name_list.append(row)

# convert list of lists to kv objects format {<name>: <csv Index>}
for i, sublist in enumerate(char_name_list):
    for name in sublist:
        charNameDict[name] = i

def userInputToCharacter(userInput):
    if userInput.lower() not in charNameDict.keys():
        raise Exception(f'{userInput} is an invalid character name')
    return char_lookup(LookupDicts.CHAR_NAME, charNameDict[userInput.lower()])


if __name__ == '__main__':
    print(userInputToCharacter('luigi'))