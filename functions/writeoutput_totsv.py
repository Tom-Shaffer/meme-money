import csv
import datetime
import os

def WriteOutput_ToTSV(symbolDict: dict(), nDays: int):
    print("Writing the company data to .TSV")
    filePath = str(datetime.date.today()) + '_' + str(nDays) + 'day_output.tsv'
    if os.path.exists(filePath):
        os.remove(filePath)
    with open(filePath, 'x') as out_file:
        listOfHeaders = list()
        listOfHeaders.append("Symbol")
        listOfHeaders.append("HitsOnWSB")
        for ad in symbolDict[0][1].additionalData.keys():
            listOfHeaders.append(ad)
        tsv_writer = csv.writer(out_file,delimiter='\t')
        tsv_writer.writerow(listOfHeaders)
        for i in symbolDict:
            listOfData = list()
            listOfData.append(i[1].symbol)
            listOfData.append(i[1].hitsOnSubreddit)
            for ad in i[1].additionalData.values():
                listOfData.append(ad)
            tsv_writer.writerow(listOfData)
    print("Complete!! Output file is located at the following:\n" + filePath)