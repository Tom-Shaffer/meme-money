import calendar
import datetime
import time
import requests
import urllib
from functions.progressbar import printProgressBar

def ExtractCurrentUTCTime() -> int:
        date = datetime.datetime.utcnow()
        return calendar.timegm(date.utctimetuple())



class APICallerWSB:
    def __FindUTCTimeToLookAfter(self) -> int:
        return ExtractCurrentUTCTime() - self.daysToLookBack*86400
    def __init__(self,symbolDictionary: dict(),daysToLookBack: int):

        self.currentRequest = ""
        self.PARAMS = dict()
        self.symbolDict = symbolDictionary
        self.domain = "https://api.pushshift.io"
        self.apiTarget = ""
        self.usefulFieldsToScrape = ""
        self.subreddit = "wallstreetbets"
        self.sort = "desc"
        self.sort_type = "created_utc"
        self.lastRequestTime = time.time()
        self.daysToLookBack = daysToLookBack
        self.lookAfter = self.__FindUTCTimeToLookAfter()
        self.lookBefore = ExtractCurrentUTCTime() 
        self.querySize = 100
        self.totalTimePeriod = self.lookBefore - self.__FindUTCTimeToLookAfter()
        self.failedAPICalls = 0
        self.searchedComments = False
        self.searchedSubmissions = False

    def CollectAllDataAfterNDaysAgo(self):
        self.SearchSubmissionAfterNDaysAgo()
        self.SearchCommentsAfterNDaysAgo()
        return self.symbolDict
    def SearchSubmissionAfterNDaysAgo(self):
        self.apiTarget = "/reddit/search/submission/"
        self.usefulFieldsString = "title,selftext,created_utc"
        self.__CollectDataAfterNDaysAgo()
        self.searchedSubmissions = True
        return self.symbolDict
    def SearchCommentsAfterNDaysAgo(self):
        self.apiTarget = "/reddit/search/comment/"
        self.usefulFieldsString = "body,created_utc"
        self.__CollectDataAfterNDaysAgo()
        self.searchedComments = True
        return self.symbolDict
    
    def __CollectDataAfterNDaysAgo(self):
        mainPrintString = "\nProcessing " + str(self.apiTarget.split('/')[-2]) + "s from WSB subredddit in the past "
        print(mainPrintString + str(self.daysToLookBack) + " days" if self.daysToLookBack > 1 else mainPrintString + "day")
        self.__CallAPI()
        self.__ResetAPIAttributes()
    def __CallAPI(self):
        if self.apiTarget == "":
            return False
        requestEmpty = False
        while self.failedAPICalls < 900 and requestEmpty == False:
            self.__FormRequest()
            requestSuccess = self.__ExecuteRequest()
            if requestSuccess:
                requestEmpty = self.__CollectDataFromRequest()
        printProgressBar(self.totalTimePeriod, self.totalTimePeriod)      
    def __FormRequest(self):
            # defining a params dict for the parameters to be sent to the API
            self.PARAMS = {
                'subreddit':self.subreddit,
                'sort':self.sort,
                'sort_type':self.sort_type,
                'after':self.lookAfter,
                'before':self.lookBefore,
                'size':self.querySize,
                'fields':self.usefulFieldsString
                }
            #Check time to ensure that we only call one time per second
            elapsed_time = time.time() - self.lastRequestTime
            if elapsed_time < 1:
                time.sleep(1 - elapsed_time)
    def __ExecuteRequest(self) -> bool:
        # sending get request and saving the response as response object
            self.currentRequest = requests.get(url = self.domain + self.apiTarget, params = urllib.parse.urlencode(self.PARAMS, safe=','))
            self.lastRequestTime = ExtractCurrentUTCTime()
            if self.currentRequest.status_code < 200 or self.currentRequest.status_code >= 300:
                print("Failed API call: " + str(self.currentRequest.status_code) + " status code." + ' ' * 100, end = "\r")
                if self.failedAPICalls < 900:
                    # Retry the API calls for up to 15 minutes
                    time.sleep(1)
                    print("... Trying again ( " + str(self.failedAPICalls) + " / 900 )" + " ..." + ' ' * 100,end = "\r")
                    self.failedAPICalls += 1
                    return False
                else:
                    # API critically failed -- Close program
                    print("Closing program... (press enter to continue)")
                    input()
                    exit
            return True
    def __CollectDataFromRequest(self):
        # extracting data in json format
        data = self.currentRequest.json()
        if len(data['data']) == 0:
            return True
        for props in data['data']:
            for prop in props:
                if prop == "created_utc":
                    # Log latest time
                    latestUTCTime = props[prop]
                    continue
                else:
                    self.__CollectData_Sentences(props[prop])
            self.lookBefore = latestUTCTime
        currentTime = ExtractCurrentUTCTime()
        printProgressBar(currentTime - latestUTCTime, self.totalTimePeriod)
        return False
    def __CollectData_Sentences(self,StringToParse):
        tmpWords = StringToParse.split()
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
                if w in self.symbolDict.keys() or "$" + w in self.symbolDict.keys() :
                    # Ticker Symbol match
                    self.symbolDict[w].hitsOnSubreddit += 1
    def __ResetAPIAttributes(self):
        self.lookAfter = self.__FindUTCTimeToLookAfter()
        self.lookBefore = ExtractCurrentUTCTime()
        self.lastRequestTime = ExtractCurrentUTCTime()
        self.failedAPICalls = 0
        self.currentRequest = ""
        self.apiTarget = ""
        self.usefulFieldsToScrape = ""
