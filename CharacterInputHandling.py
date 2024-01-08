import csv
import RioStatsConverter

charNameDict = {}
char_name_list = []

with open('CharNames.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        char_name_list.append(row)

# convert list of lists to kv objects format {<name>: <csv Index>}
for i, sublist in enumerate(char_name_list):
    for name in sublist:
        charNameDict[name] = i

def userInputToCharacter(userInput):
    if userInput not in charNameDict.keys():
        raise Exception(f'{userInput} is an invalid character name')
    return RioStatsConverter.char_id(charNameDict[userInput])


if __name__ == '__main__':
    print(userInputToCharacter('luigi'))