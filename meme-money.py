from dbm import ndbm
import requests
import datetime
import calendar
import urllib
import time
import csv
import json
import os

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()
def ExtractUserDays() -> int:
    """Extract the amount of days the user wants to look back and search the r/WallStreetBets subreddit"""

    print("Get ready to get some meme-money!! Lets see what has been going on with r/WallStreetBets!!")
    print("How many days do you want me to look back to find those juicy hot stock tips?")
    numDays = input()
    while not numDays.isdigit() or int(numDays) < 1:
        #Ensure integer value was entered
        print("Please enter a whole number of days greater than 0")
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
    
    print("\nGenerating stock data...")
    keywordLookup = dict()
    bannedWordList = list()

    #Populate the banned word list based on english prepositions
    with open('exclusions.json') as prepoFile:
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
            keywordLookup["$" + lcontent[0]] = newStock 
            companyWords = lcontent[1].split()      # Company words (in the name) are split to be added
            for cw in companyWords:
                cwLower = cw.lower()
                if cwLower in bannedWordList:
                    continue
                if cwLower in keywordLookup:
                    # We ban the word since it has already occured
                    bannedWordList.append(cwLower)
                    keywordLookup.__delitem__(cwLower)
                    continue
                keywordLookup[cwLower] = newStock
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
        
        mainPrintString = "\nProcessing " + str(command) + "s from WSB subredddit in the past "
        print(mainPrintString + str(nDays) + " days" if nDays > 1 else mainPrintString + "day")
        URL = "https://api.pushshift.io" + apiTarget
    
        date = datetime.datetime.utcnow()
        current_utc_time = calendar.timegm(date.utctimetuple())
        lastRequestTime = time.time()

        subreddit = "wallstreetbets"
        sort = "desc"
        sort_type = "created_utc"
        after = current_utc_time - nDays*86400
        before = current_utc_time
        size = 100

        totalTimePeriod = before - after
        while True:
            # defining a params dict for the parameters to be sent to the API
            PARAMS = {'subreddit':subreddit,'sort':sort,'sort_type':sort_type,'after':after,'before':before,'size':size,"fields":usefulFieldsString}
            
            #Check time to ensure that we only call one time per second
            elapsed_time = time.time() - lastRequestTime
            if elapsed_time < 1:
                time.sleep(1 - elapsed_time)

            # sending get request and saving the response as response object
            r = requests.get(url = URL, params = urllib.parse.urlencode(PARAMS, safe=','))
            if r.status_code < 200 and r.status_code >= 300:
                print("Failed API call: " + r.status_code + " status code. Try API call manually with the following link:\n" + r.url)
                print("Closing program... (press enter to continue)")
                holdopen = input()
                exit
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
                            if w.upper() == w:
                                # Ticker Symbol match
                                if w in keywordDict.keys():
                                    keywordDict[w].HitsOnWSB += 1
                            if w.lower() in keywordDict.keys():
                                # Generic word match
                                keywordDict[w.lower()].HitsOnWSB += 1
                before = latestUTCTime
            printProgressBar(current_utc_time - latestUTCTime, totalTimePeriod)
        printProgressBar(totalTimePeriod, totalTimePeriod)
    executeAPICalls("submission")
    executeAPICalls("comment")
def WriteOutputTSC(clist, nDays):

    print("Writing the company data to .TSV")
    filePath = str(datetime.date.today()) + '_' + str(nDays) + 'day_output.tsv'
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
    WriteOutputTSC(companyList,nDays)

    


if __name__ == "__main__":
    main()