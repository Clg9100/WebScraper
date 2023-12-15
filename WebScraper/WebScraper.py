import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def main():
    valid = False
    while not valid:
        filter = input("Enter your clothes filter search (Male/Female/Unisex/NONE)"
                       " or leave blank for no filter:  ")
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
        item = item.lower()
        terms = len(item.split(","))
        commas = 0

        for i in item.split(","):
            search_items.add(i)

        if terms == len(search_items):
            inputting = False
        else:
            search_items.clear() #Empty the set
            print("Invalid entry, make sure you don't duplicate search terms\n"
                  "and make sure they're seperated by commas!")
            print("\n")

    gatherAsos(filter,search_items)

def gatherAero():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

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
    wait = WebDriverWait(driver, 2)

    searchesToMake = len(items)
    ##Make a list of url's to be scraped depending on how many
    ##Search terms were recieved
    searchList = [default_url] * searchesToMake

    #Populate a list of urls to search given search terms
    for i in range(0,searchesToMake):
        searchList[i] += items.pop().strip(" ")

    for search in range(0,len(searchList)):
        driver.get(searchList[search])

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
                break

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
                break

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
                break

        expand_count = 0
        while expand_count <=5: #Could do this infinitely, but UP TO 500 items is a good sample size
            try:
                wait.until(EC.presence_of_element_located((By.CLASS_NAME,"loadButton_wWQ3F")))#Wait until load button located
                button = driver.find_element(By.CLASS_NAME, "loadButton_wWQ3F")
                driver.execute_script("arguments[0].click();", button) #Click loadmore
                expand_count +=1 #Increase page expanse by 1
            except NoSuchElementException:
                #Button doesn't exist (Exhausted or never existed)
                break
            except TimeoutException:
                # Page can't expand that many times
                break

        ##This section prints the price of each entry on the page
        the_prices = driver.find_elements(By.CLASS_NAME, "originalPrice_SOu7v")
        print(len(the_prices))
        for price in the_prices:
            print(price.get_attribute("innerText"))

        # The following code section finds all the Product links for the current page (The URLS)
        the_links = driver.find_elements(By.CLASS_NAME, "productLink_KM4PI")
        for link in the_links:
            print(link.get_attribute("href"))

        # This section of code prints ALL the product names on the CURRENT page
        product_name = driver.find_elements(By.CLASS_NAME, "productDescription_sryaw")
        for product in product_name:
            print(product.get_attribute("innerText"))

main()







