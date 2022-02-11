from functions.extractnumday import ExtractNumDaysToLookBack
from functions.getsymbols import GetSymbols
from functions.scrapewsb import ScrapeWallStreetBetsSubreddit
from functions.writeoutput_totsv import WriteOutput_ToTSV

def SearchForSymbolsInSubreddit(symbolDict: dict(), numberOfDays) -> dict():
    ScrapeWallStreetBetsSubreddit(symbolDict, numberOfDays)
    return sorted(symbolDict.items(),key=lambda x: x[1].hitsOnSubreddit, reverse=True)

def main():
    numOfDays = ExtractNumDaysToLookBack()
    searchDataDict = SearchForSymbolsInSubreddit(GetSymbols(),numOfDays)
    WriteOutput_ToTSV(searchDataDict,numOfDays)

if __name__ == "__main__":
    main()