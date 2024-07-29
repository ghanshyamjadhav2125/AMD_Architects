from selenium import webdriver
from selenium.webdriver.common.by import By
import time
driver=webdriver.Chrome()
driver.get("https://www.1mg.com/categories/homeopathy-57")



dic={"name":[],'size_of_the_bottle': [], 'MRP_of_the_bottle': [], 'price_of_the_bottle': [], '1mg_url': [], 'rating': [], 
            'number_of_rating': []}
for k in range(1,4):
    elements=driver.find_elements(By.CLASS_NAME, "col-md-3.col-sm-4.col-xs-6.style__container___1TL2R")
    for i in elements:
        try:
            dic["name"].append(i.find_element(By.CLASS_NAME,"style__pro-title___2QwJy").text)
        except:
            dic["name"].append("N/A")
        try:
            dic['size_of_the_bottle'].append(i.find_element(By.CLASS_NAME,"style__pack-size___2JQG7").text)
        except:
            dic['size_of_the_bottle'].append("N/A")
        try:
            dic['MRP_of_the_bottle'].append(i.find_element(By.CLASS_NAME,"style__discount-price___25Bya").text)
        except:
            dic['MRP_of_the_bottle'].append(i.find_element(By.CLASS_NAME,"style__price-tag___cOxYc").text)
        try:
            dic['price_of_the_bottle'].append(i.find_element(By.CLASS_NAME,"style__price-tag___cOxYc").text)
        except:
            dic['price_of_the_bottle'].append("N/A")
        try:
            dic['1mg_url'].append(i.find_element(By.CLASS_NAME,"style__product-link___UB_67").get_attribute("href"))
        except:
            dic["1mg_url"].append("N/A")
        try:
            dic["rating"].append(i.find_element(By.CLASS_NAME,"CardRatingDetail__weight-700___27w9q").text)
        except:
            dic["rating"].append("0")
        try:
            dic["number_of_rating"].append(i.find_element(By.CLASS_NAME,"CardRatingDetail__ratings-header___2yyQW").text)
        except:
            dic["number_of_rating"].append("0")
        
    driver.find_element(By.CLASS_NAME,"button-text.link-next").click()
    time.sleep(10)

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
import re


def get_element_text(by, value):
    try:
        return driver.find_element(by, value).text
    except NoSuchElementException:
        return " "

remain_values = {
    "name": [],
    "brand_name": [],
    "key_benefits": [],
    "key_ingredients": [],
}
for url in data["1mg_url"]:
    driver.get(url)
    key_ingredients = []
    key_benefits = []
    name_brand_added = False

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,'ProductTitle__product-title___3QMYH')))
        product_name = get_element_text(By.CLASS_NAME, 'ProductTitle__product-title___3QMYH')
        brand_name = get_element_text(By.CLASS_NAME, 'ProductTitle__marketer___7Wsj9')
        
        remain_values["name"].append(product_name)
        remain_values["brand_name"].append(brand_name)
        name_brand_added = True

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//b[following-sibling::ul] | //strong[following-sibling::ul]"))
        )
        headings_and_lists = driver.find_elements(By.XPATH, "//b[following-sibling::ul] | //strong[following-sibling::ul]")

        for heading in headings_and_lists:
            heading_text = heading.text.lower()
            following_siblings = heading.find_elements(By.XPATH, "following-sibling::*")

            for sibling in following_siblings:
                if sibling.tag_name in ("b", "strong"):
                    break
                if sibling.tag_name == "ul":
                    if "ingredients" in heading_text:
                        key_ingredients.extend([li.text for li in sibling.find_elements(By.TAG_NAME, "li")])
                    elif "benefits" in heading_text:
                        key_benefits.extend([li.text for li in sibling.find_elements(By.TAG_NAME, "li")])

    except TimeoutException:
        print(f"Timed out waiting for elements on page: {url}")
        if not name_brand_added:
            remain_values["name"].append("")
            remain_values["brand_name"].append("")

    except NoSuchElementException as e:
        print(f"Element not found: {str(e)}")
        if not name_brand_added:    
            remain_values["name"].append("")
            remain_values["brand_name"].append("")

    if not key_ingredients:
        try:
            prod_des = driver.find_element(By.CLASS_NAME,'ProductDescription__description-content___A_qCZ').text
        except:
            prod_des=" "
        pattern = re.compile(r'key_ingredients?:\s*((?:.+\n?)+)(?=\n\n|Key Benefits:|Directions For Use:|Safety Information:|Indications:)')
        match = pattern.search(prod_des)
        if match:
            key_ingredients = match.group(1).strip().splitlines()
            remain_values["key_ingredients"].append(key_ingredients)
        else:
            remain_values["key_ingredients"].append([])
        
    else:
        remain_values["key_ingredients"].append(key_ingredients)

    if not key_benefits:
        remain_values["key_benefits"].append([])
    else:
        remain_values["key_benefits"].append(key_benefits)

    time.sleep(2)

driver.quit()
