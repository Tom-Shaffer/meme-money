from email import header
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
    while not numDays.isdigit():
        #Ensure integer value was entered
        print("Please enter a whole number of days greater than 0")
        numDays = input()
    return int(numDays)
def parseSearchData(symbolList) -> dict():
    """Loads keyword dictionary based on the data in stockdata.tsv"""

    class symbolInfo:
        """Gives data on a given stock, described by it's ticker symbol, name, industry, and market capitalization"""
        def __init__(self, symbol, additionalData: dict()):
            self.Symbol = symbol                    # Stock's ticker symbol
            self.HitsOnWSB = 0                      # Keeps track of popularity in terms of references on WallStreetBets
            if additionalData:
                self.AdditionalData = additionalData    # Takes all the user's extra columns for association with the symbol
    
    print("\nGenerating stock data...")
    symbolDict = dict()
    with open('searchdata.tsv') as src:
        lines = src.readlines()
        header = lines[0].split('\t')
        symbolCount = len(lines)
        for l in lines[1:]:
            lcontent = l.split('\t')
            if len(lcontent) > 1:
                rowData = dict()
                i = 1
                for c in lcontent[1:]:
                    rowData[header[i]] = c.strip('\r')
                    i += 1
            newSymbol = symbolInfo(lcontent[0],rowData)
            symbolDict[lcontent[0]] = newSymbol
            symbolList.append(newSymbol)
    return symbolDict
            
    print("Symbols and their data columns allocated for " + str(symbolCount) + " symbols.")
def ParseWSB(symbolDict,nDays):
    """Parses the r/WallStreetBets subreddit using the symbols, adds the number of hits to symbolInfo class"""
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
        failIter = 0            # Counts how many times the API has failed in a row.
        while True:
            # defining a params dict for the parameters to be sent to the API
            PARAMS = {'subreddit':subreddit,'sort':sort,'sort_type':sort_type,'after':after,'before':before,'size':size,"fields":usefulFieldsString}
            
            #Check time to ensure that we only call one time per second
            elapsed_time = time.time() - lastRequestTime
            if elapsed_time < 1:
                time.sleep(1 - elapsed_time)

            # sending get request and saving the response as response object
            r = requests.get(url = URL, params = urllib.parse.urlencode(PARAMS, safe=','))
            if r.status_code < 200 or r.status_code >= 300:
                print("Failed API call: " + str(r.status_code) + " status code." + ' ' * 100, end = "\r")
                if failIter < 900:
                    # Retry the API calls for up to 15 minutes
                    time.sleep(1)
                    print("... Trying again ( " + str(failIter) + " / 900 )" + " ..." + ' ' * 100,end = "\r")
                    continue
                else:
                    # API failed -- Close program
                    print("Closing program... (press enter to continue)")
                    input()
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
                        tmp = props[prop]
                        tmpWords = tmp.split()
                        # Verify that post/comment is not in all caps -- if so continue
                        allCapsWords = 0
                        allWords = len(tmpWords)
                        submissionInAllCaps = False
                        for w in tmpWords:
                            if w.isupper():
                                allCapsWords += 1
                                if allCapsWords > .5 * allWords:
                                    # Post/Comment is in all caps and should be thrown out
                                    submissionInAllCaps = True
                                    break
                        if submissionInAllCaps == False:
                            # Scrape all word in strings and check if any keywords exist
                            for w in tmpWords:
                                if w in symbolDict.keys() or "$" + w in symbolDict.keys() :
                                    # Ticker Symbol match
                                    symbolDict[w].HitsOnWSB += 1
                before = latestUTCTime
            printProgressBar(current_utc_time - latestUTCTime, totalTimePeriod)
        printProgressBar(totalTimePeriod, totalTimePeriod)
    executeAPICalls("submission")
    executeAPICalls("comment")
def WriteOutputTSC(symbolList, nDays):

    print("Writing the company data to .TSV")
    filePath = str(datetime.date.today()) + '_' + str(nDays) + 'day_output.tsv'
    if os.path.exists(filePath):
        os.remove(filePath)
    with open(filePath, 'x') as out_file:
        listOfHeaders = list()
        listOfHeaders.append("Symbol")
        listOfHeaders.append("HitsOnWSB")
        for ad in symbolList[0].AdditionalData.keys():
            listOfHeaders.append(ad)
        tsv_writer = csv.writer(out_file,delimiter='\t')
        tsv_writer.writerow(listOfHeaders)
        for s in symbolList:
            listOfData = list()
            listOfData.append(s.Symbol)
            listOfData.append(s.HitsOnWSB)
            for ad in s.AdditionalData.values():
                listOfData.append(ad)
            tsv_writer.writerow(listOfData)
    print("Complete!! Output file is located at the following:\n" + filePath)


def main():
    searchDataList = list()
    nDays = ExtractUserDays()
    searchDataDict = parseSearchData(searchDataList)
    ParseWSB(searchDataDict, nDays)
    searchDataList.sort(key=lambda x: x.HitsOnWSB,reverse=True)
    WriteOutputTSC(searchDataList,nDays)

    


if __name__ == "__main__":
    main()