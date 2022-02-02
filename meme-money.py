import os
import sys

def ExtractUserDays() -> int:
    #####################################################################################################
    ### Extract user request

    print("Get ready to get some meme-money!! Lets see what has been going on with r/WallStreetBets!!\n")
    print("How many days do you want me to look back from today?")
    numDays = input()
    while not numDays.isdigit():
        #Ensure integer value was entered
        print("Please enter a whole number of days")
        numDays = input()
    return int(numDays)
def LoadKeywordDict() -> dict:
    #####################################################################################################
    ### Extract stockdata.tsv to keyword lookup dict

    class stockInfo:
        """Gives data on a given stock, described by it's ticker symbol, name, industry, and market capitalization"""
        def __init__(self, symbol, companyName,industry,marketCap):
            self.Symbol = symbol                    # Stock's ticker symbol
            self.CompanyName = companyName          
            self.Industry = industry                
            self.MarketCap = marketCap              # Stock's market capitalization (company valuation via stock price * # shares that exist)
            self.HitsOnWSB = 0                      # Keeps track of popularity in terms of references on WallStreetBets
    
    print("Generating stock data...")
    keywordLookup = dict()
    bannedWordList = list()
    with open('stockdata.tsv') as src:
        lines = src.readlines()
        companyCount = len(lines)
        for l in lines:
            lcontent = l.split('\t')
            newStock = stockInfo(lcontent[0],lcontent[1],lcontent[2],lcontent[3])

            # Connect dictionary terms based on the words in the company's name.
            companyWords = lcontent[1].split()
            for cw in companyWords:
                if cw in bannedWordList:
                    continue
                if cw in keywordLookup:
                    # We ban the word since it has already occured
                    bannedWordList.append(cw)
                    keywordLookup.__delitem__(cw)
                    continue
                keywordLookup[cw] = newStock
    print("Stock data generated for " + str(companyCount) + " companies.")
    return keywordLookup
def ParseWSB(keywordDict):
    print("\n###############################\nExtracting reddit data, please wait")




def main():
    nDays = ExtractUserDays()
    keywordDict = LoadKeywordDict()
    ParseWSB(keywordDict)


    


if __name__ == "__main__":
    main()