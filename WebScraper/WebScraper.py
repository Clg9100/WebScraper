from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def gather():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 5)
    driver.get("https://www.aeropostale.com/search/?q=shirt")

    current_url = driver.current_url

    driver.implicitly_wait(5)

    driver.switch_to.frame("attentive_creative")
    driver.implicitly_wait(5)
    button = driver.find_element(By.ID,"closeIconContainer")
    button.click()
    driver.switch_to.default_content()
   # print("we here")
   # element = wait.until(EC.presence_of_element_located((By.ID, "closeIconContainer"))).click()

    #This section is for clicking load more until no longer possible
    """"
    while True:
        try:
            click_more = driver.find_element(By.CLASS_NAME, "load-more-button").click()
            print("clicked once")
            driver.implicitly_wait(5)
            # Click the button while there is an option to load more
        except NoSuchElementException:
            break;
            
    """
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






