# meme-money

Remember to invest wisely, and always stick to the fundamentals. I do not recommend using this tool for real investing.

This python project allows for stock analytics to be collected from the r/WallStreetBets subreddit by searching for specific upper-case symbols in posts and comments.

File Explaination:

YYYY-MM-DD_Xday_output.tsv
This is an example output file. The file is named by giving the current date the file was written as well as how many days it screened.

meme-money.py
The python program to run

searchdata.tsv
tab-delimited input file which allows users to supply search terms
The first column must contain the symbols (In caps) that we search WSB for. The rest of the columns can be used to keep ancillary information
