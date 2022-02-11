def ExtractNumDaysToLookBack() -> int:
    def PromptUserForDaysInput() -> str:
        greeting = "Get ready to get some meme-money!! Lets see what has been going on with r/WallStreetBets!!"
        greeting += "\r\nHow many days do you want me to look back to find those juicy hot stock tips?"
        print(greeting)
        return input()
    def RepromptUserIfNotDigit() -> str:
        print("Please enter a whole number of days greater than 0")
        return input()
    numDays = PromptUserForDaysInput()
    while not numDays.isdigit():
        numDays = RepromptUserIfNotDigit()
    return int(numDays)