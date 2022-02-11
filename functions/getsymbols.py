from io import TextIOWrapper
from classes.symbolinfo import symbolInfo

def GenerateSymbolInfo(rows: list[str],headers: list[str]) -> symbolInfo:
    if len(rows) > 1:
        row = dict()
        i = 1
        for c in rows[1:]:
            row[headers[i]] = c.strip('\r')
            i += 1
    return symbolInfo(rows[0],row)
def ExtractContent(iFile: TextIOWrapper) -> dict:
    sDict = dict()
    lines = iFile.readlines()
    headers = lines[0].split('\t')
    for l in lines[1:]:
        lineData = l.split('\t')
        symbol = GenerateSymbolInfo(lineData,headers)
        sDict[lineData[0]] = symbol
    return sDict
def OpenTSV_WriteToDict() -> dict():
    with open('searchinput.tsv') as inputFile:
        return ExtractContent(inputFile)
    

def GetSymbols() -> dict():
    print("\nGenerating stock data...")
    symbolDict = OpenTSV_WriteToDict()
    print("Symbols and their data columns allocated for " + str(len(symbolDict)) + " symbols.")
    return symbolDict