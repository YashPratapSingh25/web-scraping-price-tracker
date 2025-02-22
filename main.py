from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from amazoncaptcha import AmazonCaptcha

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

def amazon_scraping(search_query):
    driver.get("https://www.amazon.in/")

    try:
        captcha_link = driver.find_element(By.TAG_NAME, "img").get_attribute("src")
        captcha = AmazonCaptcha.fromlink(captcha_link)
        captcha_value = AmazonCaptcha.solve(captcha)

        captcha_text_field = driver.find_element(By.ID, "captchacharacters")
        captcha_text_field.send_keys(captcha_value)

        button = driver.find_element(By.TAG_NAME, "button")
        button.click()
    except:
        pass

    text_field = driver.find_element(By.ID, "twotabsearchtextbox")
    text_field.send_keys(search_query + Keys.ENTER)

    products = driver.find_elements(By.CSS_SELECTOR, "div[role='listitem']")

    i = 0
    products_shown = 0
    while products_shown < 5:

        product_image = products[i].find_element(By.CSS_SELECTOR, "img.s-image").get_attribute("src")

        product_name = products[i].find_element(By.CSS_SELECTOR, "div[role='listitem'] h2.a-color-base").get_attribute("aria-label")

        try:
            product_price = products[i].find_element(By.CSS_SELECTOR, "span.a-price-whole").text
        except:
            i += 1
            continue

        product_link = products[i].find_element(By.CSS_SELECTOR, "a.a-link-normal").get_attribute("href")

        if product_name.find("Sponsored Ad") == 0:
            i += 1
            continue

        print("Product Image:", product_image)
        print("Product Title:", product_name)
        print("Product Price:", product_price)
        print("Product Link:", product_link)
        print("")

        i += 1
        products_shown += 1


def flipkart_scraping(search_query : str):
    driver.get("https://www.flipkart.in/")

    text_field = driver.find_element(By.CSS_SELECTOR, "input[title = 'Search for Products, Brands and More']")
    text_field.send_keys(search_query + Keys.ENTER)

    is_grid = True
    products = driver.find_elements(By.CLASS_NAME, "slAVV4")

    if len(products) == 0:
        is_grid = False
        products = driver.find_elements(By.CLASS_NAME, "tUxRFH")

    i = 0
    products_shown = 0

    while products_shown < 5:

        try:
            products[i].find_element(By.CSS_SELECTOR, "div.f8qK5m")
            i += 1
            continue
        except:
            pass

        if is_grid:
            product_image = products[i].find_element(By.CSS_SELECTOR, "img.DByuf4").get_attribute("src")
            product_name = products[i].find_element(By.CSS_SELECTOR, "a.wjcEIp").get_attribute("title")
            product_price = products[i].find_element(By.CSS_SELECTOR, "div.Nx9bqj").text
            product_link = products[i].find_element(By.CSS_SELECTOR, "a.VJA3rP").get_attribute("href")
        else:
            product_image = products[i].find_element(By.CSS_SELECTOR, "img.DByuf4").get_attribute("src")
            product_name = products[i].find_element(By.CSS_SELECTOR, "div.KzDlHZ").text
            product_price = products[i].find_element(By.CSS_SELECTOR, "div.Nx9bqj").text
            product_link = products[i].find_element(By.CSS_SELECTOR, "a.CGtC98").get_attribute("href")

        print("Product Image:", product_image)
        print("Product Name:", product_name)
        print("Product Price:", product_price)
        print("Product Link:", product_link)
        print("")

        i += 1
        products_shown += 1




print("Welcome to Price Tracker")
search_query = input("Enter product name: ").strip().lower()

amazon_scraping(search_query)
flipkart_scraping(search_query)

time.sleep(60)

driver.quit()