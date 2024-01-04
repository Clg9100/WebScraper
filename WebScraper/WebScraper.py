import time
import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main():
    valid = False
    while not valid:
        filter = input("Enter your clothes filter search (Male/Female/Unisex/NONE)"
                       " or NONE for no filter:  ")
        print(filter.upper())
        if (filter.upper() == "MALE" or filter.upper() == "FEMALE"
                or filter.upper() == "NONE") or filter.upper() == "UNISEX":
            valid = True
            if filter.upper() == "MALE":
                print("Searching clothes by " + filter + " filter search")
            elif filter.upper() == "FEMALE":
                print("Searching clothes by " + filter + " filter search")
            elif filter.upper() == "UNISEX":
                print("Searching clothes by " + filter + " filter search")
            else:
                print("Searching with no filter...")

        else:
            print("Invalid filter try again")

    filter=filter.upper() #Normalize user input

    search_items = set()
    inputting = True

    ##One bug for input in this section that's known is
    ##If user enters search terms such as "Shirt shirt shirt pants
    #Without commas this will count as one search term
    while(inputting):
        item = input("Enter the items you want to search for as a comma seperated list -\n"
                     "(EX: Shirts, pants, hats, dresses: ")
        print("\n")
        item = item.lower()
        terms = len(item.split(","))
        onlyStrings = True

        for i in item.split(","):
            if(i.strip(" ").isdigit()): #Check to make sure user has entered valid input
                onlyStrings = False #Found an int, invalid input
                break #No need to add search items, invalid input
            search_items.add(i)

        if terms == len(search_items) and onlyStrings == True:
            inputting = False
        else:
            search_items.clear() #Empty the set
            print("Invalid entry, make sure you don't duplicate search terms\n"
                  "and make sure they're separated by commas! (No numbers!)")
            print("\n")

    createCSVHeader()  # Create csv file with just this header
    # Get data from site and create csv file from that data
    # returns a dict of budgets to form budget csv
    budgets = gatherAsos(filter,search_items)
    createBudgetCSV(budgets) # Create the csv file for products that fit within budget
    print("All items that fit your initial queries on your chosen filter can be found in the file: fullData.csv")
    print("All items that are under your entered per item budget can be found in the file: budgetData.csv")

def gatherAero():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 5)

    driver.get("https://www.aeropostale.com/search/?q=shirt")

    driver.implicitly_wait(60)

    driver.switch_to.frame("attentive_creative") #Switch frame to close ad
    driver.implicitly_wait(5)
    button = driver.find_element(By.ID,"closeIconContainer") #Find ad
    button.click() # Close ad
    driver.switch_to.default_content() #Switch back to original frame

    #This section is for clicking load more until no longer possible

    time.sleep(5)
    # button = driver.find_element(By.XPATH, "//*[@id='primary']/div[1]/div[2]/div/div")
    # print(button)
    # driver.execute_script("arguments[0].click();", button)
    # print("clicked")

    while True:
        try:
            #wait.until(EC.element_to_be_clickable((By.XPATH,"//*[@id='primary']/div[1]/div[2]/div/div")))
            button = driver.find_element(By.XPATH,"//*[@id='primary']/div[1]/div[2]/div/div")
            driver.execute_script("arguments[0].click();",button)
            time.sleep(10)
        except Exception as e:
            print(e)
            break

    ##This section prints the price of each entry on the page
    the_prices = driver.find_elements(By.CLASS_NAME,"product-pricing")
    for price in the_prices:
        print(price.get_attribute("innerText"))

    #The following code section finds all the Product links for the current page (The URLS)
    the_links = driver.find_elements(By.CLASS_NAME,"thumb-link")
    for link in the_links:
        print(link.get_attribute("href"))


    #This section of code prints ALL the product names on the CURRENT page
    product_name = driver.find_elements(By.CLASS_NAME,"product-name")
    for product in product_name:
        print(product.get_attribute("innerText"))

    driver.close()


def gatherAsos(filter,items):##Seemingly a GOOD website thus far

    # driver.get("https://www.asos.com/us/search/?q=shirt")
    # driver.get("https://www.asos.com/us/search/?q=gloves")
    default_url = "https://www.asos.com/us/search/?q="
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    searchesToMake = len(items) # Record searches to make given search terms
    ##Make a list of url's to be scraped depending on how many
    ##Search terms were recieved
    searchList = [default_url] * searchesToMake

    #Populate a list of urls to search given search terms
    for i in range(0,searchesToMake):
        searchList[i] += items.pop().strip(" ")


    for search in range(0,len(searchList)):
        driver.get(searchList[search])
        print("Currently printing info for "+searchList[search])

        if filter == "MALE":
            try: #Gotta check to see if the item allows sorting by gender
                wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='plp']/div/div[2]/div/div/div[1]/ul/li[3]/div")))  # Wait until gender filter button clickable
                button = driver.find_element(By.XPATH, "//*[@id='plp']/div/div[2]/div/div/div[1]/ul/li[3]/div")
                ##Checking the button to make sure it's the gender filter, otherwise item doesn't offer that filter
                if button.text == "Gender":
                    button.click()
                    wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='plp']/div/div[2]/div/div/div[1]/ul/li[3]/div/div/div/ul/li[1]/div/label/div")))
                    button = driver.find_element(By.XPATH,"//*[@id='plp']/div/div[2]/div/div/div[1]/ul/li[3]/div/div/div/ul/li[1]/div/label/div")
                    button.click()
                else:
                    raise NoSuchElementException #Item doesn't have that filter

            except NoSuchElementException:
                print("This item doesn't have that filter, using no filter")
            except TimeoutException: #No search results found for this item
                print("This search produced no results")
                continue

        elif filter == "FEMALE":
            try: #Gotta check to see if the item allows sorting by gender
                wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='plp']/div/div[2]/div/div/div[1]/ul/li[3]/div")))  # Wait until gender filter button clickable
                button = driver.find_element(By.XPATH, "//*[@id='plp']/div/div[2]/div/div/div[1]/ul/li[3]/div")
                if button.text == "Gender":
                    button.click()
                    wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='plp']/div/div[2]/div/div/div[1]/ul/li[3]/div/div/div/ul/li[2]/div/label/div")))
                    button = driver.find_element(By.XPATH,"//*[@id='plp']/div/div[2]/div/div/div[1]/ul/li[3]/div/div/div/ul/li[2]/div/label/div")
                    button.click()
                else:
                    raise NoSuchElementException #Item doesn't have that filter
            except NoSuchElementException:
                print("This item doesn't have that filter, using no filter")
            except TimeoutException: #No search results found for this item
                print("This search produced no results")
                continue

        elif filter == "UNISEX":
            try: #Gotta check to see if the item allows sorting by gender
                wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='plp']/div/div[2]/div/div/div[1]/ul/li[3]/div")))  # Wait until gender filter button clickable
                button = driver.find_element(By.XPATH, "//*[@id='plp']/div/div[2]/div/div/div[1]/ul/li[3]/div")
                if button.text == "Gender":
                    button.click()
                    wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='plp']/div/div[2]/div/div/div[1]/ul/li[3]/div/div/div/ul/li[3]/div/label/div")))
                    button = driver.find_element(By.XPATH,"//*[@id='plp']/div/div[2]/div/div/div[1]/ul/li[3]/div/div/div/ul/li[3]/div/label/div")
                    button.click()
                else:
                    raise NoSuchElementException #Item doesn't have that filter
            except NoSuchElementException:
                print("This item doesn't have that filter, using no filter")
            except TimeoutException: #No search results found for this item
                print("This search produced no results")
                continue

        expand_count = 0 #Amount of times to click show more on page
        while expand_count <2: #Could do this infinitely, but UP TO 500 items is a good sample size( < 2 = 216 results or less)
            try:
                button = driver.find_element(By.CLASS_NAME, "loadButton_wWQ3F")
                driver.execute_script("arguments[0].click();", button)  # Click loadmore
                wait.until(EC.presence_of_element_located((By.CLASS_NAME,"loadButton_wWQ3F")))#Wait until load button located
                expand_count += 1  # Increase page expanse by 1

                # """
                # Holding this code because not sure if I still need it
                # Was buggy such that we would start grabbing elements before the page source was loaded after clicking show more,
                # Thusly leading to index out of bound errors on our data lists
                # button = driver.find_element(By.CLASS_NAME, "loadButton_wWQ3F")
                # driver.execute_script("arguments[0].click();", button) #Click loadmore
                # expand_count +=1 #Increase page expanse by 1
                # driver.implicitly_wait(20) #Need to add wait, otherwise data lists won't fill right
                # """

            #Specifically for case that 'load more' can be clicke no more, or merely doesn't exist on the page
            except NoSuchElementException:
                #Button doesn't exist (Exhausted or never existed)
                break
            except TimeoutException:
                # Page can't expand that many times
                break
        driver.implicitly_wait(10)

        #Instantiate the lists to hold product data
        discountPriceList = [] #Contains ALL prices (Discounted and otherwise)
        priceList = [] #Contains ALL prices (However only their original price, doesn't account for discount price
        urlList = [] #Contains Url of all products on current item being searched page.
        nameList = []#Contains name of every product found by current search term

        #This section prints the price of each entry on the page

        #Use this for current price, factoring in sales(RRP)
        the_prices = driver.find_elements(By.CLASS_NAME, "originalPrice_SOu7v")#Prices before discount (Baseline prices)
        driver.implicitly_wait(10)

        #BREAKTHROUGH - THIS GETS ALL PRICES ON THE PAGE, JUST HAVE TO CLEAN THE TEXT GIVEN
        all_prices = driver.find_elements(By.XPATH, "//p[contains(@aria-label, 'price') or contains(@aria-label,'Price')]")  # Discounted prices

        ##Use this for strictly original price
        ##the_prices = driver.find_elements(By.CLASS_NAME, "price_CMH3V")

        #print(len(the_prices))

        #For each price element, add its price to price list
        for price in the_prices:
            #print(price.get_attribute("innerText"))
            priceList.append(price.get_attribute("innerText"))


        #print("All prices length: "+str(len(all_prices)))
        #For each discount price element, add its price to discounted price list
        for price in all_prices:
            thePrice = price.get_attribute("innerText")
            ##Testing purpose print
            #print("Inner text given = "+thePrice)
            #Now we do validation on the string we got on a case by case scenario, three cases are:
            #It's a Recommended retail price item of the form RRP $xx.xx$xx.xx
            #Its an item not on sale of the form $xx.xx
            #It's an item on sale, but not recommended retail price discounted of the form $xx.xx$xx.xx

            if(thePrice[0] == "$"):
                cashCount = 0 #How many $ symbols
                iter = 0 #For indexing the string
                #Count how many cash symbols to determine if it's a $xx.xx form price, or a $xx.xx$xx.xx form price
                for character in thePrice:
                    if(character == "$"):
                        cashCount+=1
                    # Is a discounted item, just have to make sure we take the discounted price now with slicing
                    # Is of the format: $xx.xx$xx.xx
                    if(cashCount == 2):
                        discountPriceList.append(thePrice[iter:])
                        break #We can move on to next one
                    iter += 1
                    #print("Iterator is: " +str(iter))

                ## If we made it here, it must be of the format: $xx.xx, add it to price list
                if(cashCount < 2):
                    discountPriceList.append(thePrice)

            # There exists a special case discovered on a search of unisex pants
            # Apparently, sometimes prices come in the form: From$xx.xx, this is what thePrice[0] == F seeks to cover
            elif (thePrice[0] == "F"):
                cashCount = 0  # How many $ symbols
                iter = 0  # For indexing the string
                # Count how many cash symbols to determine if it's a $xx.xx form price, or a $xx.xx$xx.xx form price
                for character in thePrice:
                    if (character == "$"):
                        cashCount += 1
                    # Is a discounted item, just have to make sure we take the discounted price now with slicing
                    # Is of the format: $xx.xx$xx.xx
                    if (cashCount == 1):
                        discountPriceList.append(thePrice[iter:])
                        break  # We can move on to next one
                    iter += 1

            #It's a recommended retail price item, is on sale, have to clean input a bit.
            #Is of the format: RRP$xx.xx$xx.xx
            else:
                count = 0 #How many $ have we seen? We're looking for 2, by the second we know to take the price following it
                iter = 0 #For indexing the string
                for character in thePrice:
                    if(character == "$"):
                        count+=1
                    if(count == 2): #We've seen the second price now, grab it
                        discountPriceList.append(thePrice[iter:])
                        break #We've added it, we can leave
                    iter +=1 #Increment iterator

        # Testing purpose prints
        # for cleanPrice in discountPriceList:
        #     print("The Price is "+cleanPrice)
        #print("PriceList size: ")
        #print(len(priceList))

        # The following code section finds all the Product links for the current page (The URLS)
        the_links = driver.find_elements(By.CLASS_NAME, "productLink_KM4PI")
        # For each href link, add its url to the list of urls for each product
        for link in the_links:
            #print(link.get_attribute("href"))
            urlList.append(link.get_attribute("href"))

        # Testing purpose prints
        #print("LinkList size: ")
        #print(len(urlList))

        # This section of code prints ALL the product names on the CURRENT page
        product_name = driver.find_elements(By.CLASS_NAME, "productDescription_sryaw")

        #For each product add its name to list of product names
        for product in product_name:
            #print(product.get_attribute("innerText"))
            nameList.append(product.get_attribute("innerText"))

        # Testing purpose prints
        # print("nameList size: ")
        # print(len(nameList))

        #Section for combining data for transfer to csv
        data = []
        for product in range(0,len(nameList)):
            data.append([])

        #Section for cleaning data ahead of time -making sure discounted prices are reflected, and not their original price

        #Testing purpose prints
        #print(len(data))
        #print("Discount size "+ str(len(discountPriceList)))
        for eachProduct in range(0,len(data)):
            # Add search term used for this item lookup (Using list comprehension to get just the search term with split)
            data[eachProduct].append(searchList[search].split(default_url)[-1])
            data[eachProduct].append(nameList[eachProduct])#Add name of product
            #data[eachProduct].append(priceList[eachProduct]) #Add price of product (Old way, before discount validation)
            data[eachProduct].append(discountPriceList[eachProduct])# Add price of product (Latest way, actually gets discounts)
            data[eachProduct].append(urlList[eachProduct]) # Add url of product
            #print(data[eachProduct]) #to print data
        createCSV(data) #Write to the csv file the list of data for csv file creation

    itemBudgets = storeBudgets(searchList, default_url)
    #print(itemBudgets) #test to see if dict is created
    return itemBudgets


def storeBudgets(searchList, default_url):
    itemBudgets = {}
    for item in range(len(searchList)):
        inputting = True #Toggle for valid input
        while (inputting):
            #Get the users budget for the current search term item
            uiBudget = input("Enter your budget for search item - " + searchList[item].split(default_url)[-1] + ": ")
            if(uiBudget.isdigit()):
                uiBudget = int(uiBudget) # Cast it to an int, it's valid
                if(uiBudget > 0):
                    itemBudgets[searchList[item].split(default_url)[-1]] = uiBudget  # Set the users budget for the search term
                    inputting = False  # Toggle for valid input
                else:
                    print("Make sure your budget is greater than 0 and is a number! (No decimals, round up to nearest dollar)")
            else:
                print("Make sure your budget is greater than 0 and is a number!(No Decimals, round up to nearest dollar)")
    return itemBudgets #Return dictionary of item budgets


def createCSV(theData):
    with open('fullData.csv', 'a',newline='') as file:
        write = csv.writer(file)
        write.writerows(theData)
        file.close() #Close resource


def createBudgetCSV(itemBudgets):
    #budgetData = []
    createBudgetCSVHeader()  # Create csv file for budgeted items with just the header
    #Reading full data, appending to bugetData (Because it already has the header, append to it)
    with open('fullData.csv', mode='r') as infile, open ('budgetData.csv', mode='a', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        next(reader, None)  # skip the headers
        for lines in reader:
            #Testing purpose print
            #print(lines)
            #If the price of the search term item being looked at is LESS than the budget,
            # it's good to add it do our budgeted items list of data
            #Otherwise don't add it, it goes over user's budget on its own
            price = lines[2]
            # Testing purpose prints, a bit important - don't want to remove them just yet.
            #print("Search item being checked: "+lines[0])
            # print("Price of said item: "+str(price[1:]))
            # print("Budget being checked: "+str(float(itemBudgets.get(lines[0]))))

            if(float(price[1:]) < float(itemBudgets.get(lines[0]))):
                writer.writerow(lines)
                #Testing purpose print to make sure we're getting correct data
                #budgetData.append(lines)

    #Testing purpose print
    #for data in range(len(budgetData)):
        #print(budgetData[data])
        infile.close() #Close resource
        outfile.close() #Close resource

def createCSVHeader():

    if os.path.exists("fullData.csv"):
        os.remove("fullData.csv")
        print("Old CSV file deleted")
        print("Writing new csv file: fullData.csv")
        fields = ['Search Term', 'Product Name', 'Price', 'Link']  # Header row for product data listings
        with open('fullData.csv', 'w',newline='') as file:  # 'w' mode is for writing to a file
            write = csv.writer(file)
            write.writerow(fields)
            file.close()#Close resource
    else:
        print("Writing new csv file: fullData.csv")
        fields = ['Search Term', 'Product Name', 'Price', 'Link']  # Header row for product data listings
        with open('fullData.csv', 'w') as file:  # 'w' mode is for writing to a file
            write = csv.writer(file)
            write.writerow(fields)
            file.close()#Close resource


def createBudgetCSVHeader():

    if os.path.exists("budgetData.csv"):
        os.remove("budgetData.csv")
        print("Old CSV file deleted")
        print("Writing new csv file: budgetData.csv")
        fields = ['Search Term', 'Product Name', 'Price', 'Link']  # Header row for product data listings
        with open('budgetData.csv', 'w',newline='') as outfile:  # 'w' mode is for writing to a file
            write = csv.writer(outfile)
            write.writerow(fields)
            outfile.close()#Close resource
    else:
        print("Writing new csv file: budgetData.csv")
        fields = ['Search Term', 'Product Name', 'Price', 'Link']  # Header row for product data listings
        with open('budgetData.csv', 'w') as outfile:  # 'w' mode is for writing to a file
            write = csv.writer(outfile)
            write.writerow(fields)
            outfile.close()#Close resource


main()







