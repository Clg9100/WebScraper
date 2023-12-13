from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def gather():
    driver = webdriver.Chrome()

    driver.get("https://www.aeropostale.com/search/?q=shirt")

    current_url = driver.current_url

    driver.implicitly_wait(5)
    while True:
        try:
            mark_complete = driver.find_element(By.CLASS_NAME, "load-more-button")
            mark_complete.click()  # Click the button while there is an option to load more
        except NoSuchElementException:
            continue
    driver.implicitly_wait(5)

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


gather()






