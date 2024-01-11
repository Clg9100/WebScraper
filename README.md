# WarDrobe Webscraper
A WebScraping Python project 

Wardrobe is a webscraper that in its current state can be used by end users to quickly run searches for various clothes items (from the Asos.com clothing website) they may be in the market for purchasing all whilst staying within a budget imposed by the user regarding how much they're actually looking to pay for particular clothes item. 

Because this process is automated it saves the user time scrolling and scouring the website for clothes that fit the users budget, it's as simple as entering a few search criteria and sending the program on its way.


# Requirements

Just run the standalone program WardDrobe which should include all the libraries and dependencies you need for the program to run! 

**(*Not available yet*)**


# Program Rundown / Usage:
Program flow is pretty straightforward, but nontheless worth explaining including some caveats.

Upon running the program you'll be met with a prompt for which gender filter you want to (or if you don't want any filter) impose on your clothes item search:

![Webscraper filter](https://github.com/Clg9100/WebScraper/assets/33357071/ad338170-2788-45e6-b923-91d4e92af925)

Users are able to choose either Male, Female, Unisex or merely no filter for their search (Note: if you want to search for more than one filter you will have to run the program again on that filter UNLESS you don't care for any filter, in which case you would just enter none)

From there you will be prompted to enter the items you want to search for as a comma separated list like so :

![Webscraper ItemSearch](https://github.com/Clg9100/WebScraper/assets/33357071/4d84e461-c4ab-4cbc-b294-ae35e6a29c6d)

You COULD potentially search for items as a combination such as : "Shirt and Pants" however this will dillute your search and likely not give you the best results so this is not recommended.

You will then be prompted if you want your produced CSV files to include the images of the items found:

![WebscraperImages](https://github.com/Clg9100/WebScraper/assets/33357071/34c9b83a-cdd6-47d4-8b24-937b4205461a)

It's worth mentioning that by default the produced CSV files will already contain a link to the product page for each item, the inclusion of the image in the programs current state is to just give the user a quick way to view the product by including the image link without immediately going to the product page for example if they were interested in buying it just off price alone or whatever else their motivation. Opting for inclusion of images WILL make the program run a bit slower just by the nature of how they are gathered but otherwise there's no other notable drawback to including them.

Once you've decided if you want to include pictures or not the program will start opening (One at a time) automated browser windows for gathering the data like so:


![asos](https://github.com/Clg9100/WebScraper/assets/33357071/1de750cc-7d48-4d5f-901e-5d7b910665fd)

**Do not be alarmed!** 

You can even take a bit of joy in watching the program do its MAGIC, the page will scroll on its own, so be sure to not mess with or close the webpage that comes up, depending on how many items you wanted to search for in your comma seperated search items, it will search that many times within the window. You're free to minimize this window, rather ENCOURAGED to do so, but nonetheless just let it run without closing it and it'll do the work.

When its done gathering the data you will be prompted to enter a budget for each item you searched for - that is you should enter a number indicative of how much you're willing to pay MAX for each item type, make sure it's a whole number, you don't need to and actually CAN'T enter decimals:


![Webscraper Budgets](https://github.com/Clg9100/WebScraper/assets/33357071/5b34d741-5ed5-405f-9b1a-6eb0c66b5158)


When it's all done the program will hit you with the finishing text and close:

![Webscraper Finish](https://github.com/Clg9100/WebScraper/assets/33357071/954de2cc-3f3c-4f38-8fed-72ef92d63c9f)

The text regarding the old csv files being deleted will only appear on subsequent runs of the program - and on that note, if you for whatever reason want to keep the csv files produced just make sure to rename them OR move them to a different directory, otherwise they will be deleted each time the program is run.

You should be able to find your new CSV files containing the data pertaining to your searches in the two files: fullData.csv and budgetData.csv

The header for these files is of the following format: 

**Search Term, Product Name, Price, Link, (OPTIONALLY - You wanted images) ImageSrc  
*OR*  
Search Term, Product Name, Price, Link**

In Google Sheets / Excel the files will look something like this:

![WebscraperData](https://github.com/Clg9100/WebScraper/assets/33357071/e14035fc-5766-4cc9-ba7f-c2acb3781f6a)

The difference between the two csv files is that fullData.csv will contain up to 216 (Two page expansions worth) of items for each search item, whereas bugetData.csv will only include the items pulled from this full list of data for each item that fit within your imposed budget for each item.

Congratulations, you just ran a program and got data to help you make informed commercial decisions way faster than if you spent the time scrolling the site yourself!


# Errors and Bugs
Ideally, it should work; But we know this isn't always the case with software - if the program hasn't produced the expected number of results in your CSV files, hasn't gotten an image for every product, pricing information is wrong, just straight up blew up etc - it's likely due to the volatile nature of how the information is scraped. 

Run the program a few more times as something like internet speed could affect some aspects of the programs successful running (Like gathering of the images), but if the outcome remains the same please contact me as it's more than likely something about the site has changed and thusly I have to rewrite or add to the code to fix this issue - this is common and expected.

# Roadmap
I have a ton of great ideas for expanding this projects functionality some of which I'll list below but cannot promise any timeframe on when they'll be available:

- User Interface improvement

- More item search filters (Discount %, Price Range, Size, Color)

- Database storage

- Outfit creator (Items for an outfit and the total cost)

# Authors

- **Chris Grate @ Clg9100**

# Project Status
Currently adding more functionality and *maintaining*
