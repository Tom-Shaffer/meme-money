from classes.apicaller import APICallerWSB


def ScrapeWallStreetBetsSubreddit(symbolDict,nDays):
    print("\n###############################\nExtracting reddit data, please wait")
    Api = APICallerWSB(symbolDict,nDays)
    return Api.CollectAllDataAfterNDaysAgo()
    