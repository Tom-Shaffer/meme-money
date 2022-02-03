import requests
import datetime
import calendar
import urllib
import time
import csv
import json
import os

def ExtractUserDays() -> int:
    """Extract the amount of days the user wants to look back and search the r/WallStreetBets subreddit"""

    print("Get ready to get some meme-money!! Lets see what has been going on with r/WallStreetBets!!\n")
    print("How many days do you want me to look back from today?")
    numDays = input()
    while not numDays.isdigit():
        #Ensure integer value was entered
        print("Please enter a whole number of days")
        numDays = input()
    return int(numDays)
def LoadKeywordDict(companyList) -> dict:
    """Loads keyword dictionary based on the data in stockdata.tsv"""

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

    #Populate the banned word list based on english prepositions
    with open('prepositions&exclusions.json') as prepoFile:
        prepoJSON = json.load(prepoFile)
        for p in prepoJSON:
            bannedWordList.append(p)


    with open('stockdata.tsv') as src:
        lines = src.readlines()
        companyCount = len(lines)
        for l in lines:
            lcontent = l.split('\t')
            newStock = stockInfo(lcontent[0],lcontent[1],lcontent[2],lcontent[3])
            companyList.append(newStock)

            # Connect dictionary terms based on the words in the company's name and ticker.
            keywordLookup[lcontent[0]] = newStock   # Stocks ticker attached to newStock object
            companyWords = lcontent[1].split()      # Company words (in the name) are split to be added
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
def ParseWSB(keywordDict,nDays):
    """Parses the r/WallStreetBets subreddit using the keyword dictionary, adds the number of hits to the stock ino class"""
    print("\n###############################\nExtracting reddit data, please wait")

    def executeAPICalls(command):
        """Executes pushshift API calls to extract all data for either submission or comment"""
        if command == "submission":
            apiTarget = "/reddit/search/submission/"
            usefulFieldsString = "title,selftext,created_utc"
        elif command == "comment":
            apiTarget = "/reddit/search/comment"
            usefulFieldsString = "body,created_utc"
        else:
            return False

        print("Processing " + str(command) + "s from WSB subredddit in past " + str(nDays) + " days.")
        URL = "https://api.pushshift.io" + apiTarget
    
        date = datetime.datetime.utcnow()
        current_utc_time = calendar.timegm(date.utctimetuple())
        lastRequestTime = time.time()

        subreddit = "wallstreetbets"
        sort = "desc"
        sort_type = "created_utc"
        after = current_utc_time - nDays*86400
        before = current_utc_time
        size = 1000

        while True:
            # defining a params dict for the parameters to be sent to the API
            PARAMS = {'subreddit':subreddit,'sort':sort,'sort_type':sort_type,'after':after,'before':before,'size':size,"fields":usefulFieldsString}
            
            #Check time to ensure that we only call one time per second
            elapsed_time = time.time() - lastRequestTime
            if elapsed_time < 1:
                time.sleep(1 - elapsed_time)

            # sending get request and saving the response as response object
            r = requests.get(url = URL, params = urllib.parse.urlencode(PARAMS, safe=','))
            lastRequestTime = time.time()

            # extracting data in json format
            data = r.json()
            if len(data['data']) == 0:
                break
            for props in data['data']:
                for prop in props:
                    if prop == "created_utc":
                        # Log latest time
                        latestUTCTime = props[prop]
                        continue
                    else:
                        # Scrape all word in strings and check if any keywords exist
                        tmp = props[prop]
                        tmpWords = tmp.split()
                        for w in tmpWords:
                            if w in keywordDict.keys():
                                keywordDict[w].HitsOnWSB += 1
                before = latestUTCTime
        
    executeAPICalls("submission")
    executeAPICalls("comment")
def WriteOutputTSC(clist):

    print("Writing the company data to .TSV")
    filePath = str(datetime.date.today()) + '_output.tsv'
    if os.path.exists(filePath):
        os.remove(filePath)
    with open(filePath, 'x') as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')
        tsv_writer.writerow(['Symbol', 'CompanyName','Industry','MarketCap','HitsOnWSB'])
        for c in clist:
            tsv_writer.writerow([c.Symbol,c.CompanyName,c.Industry,c.MarketCap,c.HitsOnWSB])
    print("Complete!! Output file is located at the following:\n" + filePath)


def main():
    companyList = list()
    nDays = ExtractUserDays()
    keywordDict = LoadKeywordDict(companyList)
    ParseWSB(keywordDict, nDays)
    companyList.sort(key=lambda x: x.HitsOnWSB,reverse=True)
    WriteOutputTSC(companyList)

    


if __name__ == "__main__":
    main()