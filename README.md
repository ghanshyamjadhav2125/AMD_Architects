
# 1Mg Homeopathic Medicine Scraping Project

This project focuses on extracting, cleaning, and analyzing data from the 1mg homeopathic medicine website. By utilizing web scraping techniques, we aim to gather detailed information about various homeopathic medicines available on the platform. The project includes several key stages: web scraping, data cleaning, data analysis using SQL/NoSQL, and visualization. Additionally, insights are presented through a PowerPoint presentation and an interactive dashboard.

## Key Objectives:
- Web Scraping: Automate the extraction of relevant data from the 1mg website.
- Data Cleaning: Ensure the data is accurate and consistent for analysis.
- Data Analysis: Use SQL/NoSQL queries to derive meaningful insights from the data.
- Visualization: Create an interactive dashboard to visualize the data and highlight key insights.
- Presentation: Summarize the findings in a PowerPoint presentation for clear communication of results.

## Project Deliverables:
- Web Scraping Code: Python scripts using Selenium to scrape data from the 1mg website.
- Cleaned Data: A cleaned dataset saved in CSV format.
- SQL/NoSQL Queries: SQL/NoSQL scripts to analyze the cleaned data and generate insights.
- PowerPoint Presentation: Slides summarizing the project, data insights, and key findings.
- Interactive Dashboard: A dashboard for visualizing data, highlighting price distribution, top brands, average discounts, and ratings analysis.

## Table of Contents 
    1. Introduction
    2. Ethical Scraping Practices
    3. Web Scraping Implementation
    4. Data Cleaning
    5. Data Analysis
    6. Dashboard Creation
    7. Conclusion

### 1. Introduction
This project involves scraping homeopathic medicine data from the 1Mg website using Python and BeautifulSoup. The aim is to collect detailed information about various medicines and then perform data analysis to extract meaningful insights. The insights will be presented in a PowerPoint presentation, and an interactive dashboard will be created for end-users to explore the data.
    
### 2. Ethical Scraping Practices
- Adhered to ethical scraping practices and respected the website's terms of service.
- Implemented delays between requests to avoid overloading the website's servers.
- Used polite scraping techniques to minimize the load on the website's resources.

### 3. Web Scraping Implementation

#### Deployment

To run this project first you need these libraries and follow the steps mentioned

#### Libraries Nedded
- pandas for data manipulation and analysis
- numpy for numerical operations
- selenium for web scraping
- time for giving delays while scrapping
- re for regular expression operations

#### Step 1: Import libraries, initialize the WebDriver and Open the Website
```bash
    import pandas as pd
    import numpy as np
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    import time
    import re

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://www.1mg.com/categories/homeopathy-57?filter=true&page=1")

    # use the line below to close the popup window if you got.
    driver.find_element(By.CLASS_NAME, 'UpdateCityModal__update-btn___2qmN1.UpdateCityModal__btn___oMW5n').click()

```

#### Step 2: Scrape Data from Multiple Pages

```bash
    # Scrape data from multiple pages
    parent_list = []
    pages_to_scrape = 20
    for i in range(pages_to_scrape):
        parent_list += driver.find_elements(By.CLASS_NAME, 'col-md-3.col-sm-4.col-xs-6.style__container___1TL2R')
        time.sleep(3)
        driver.find_element(By.CLASS_NAME, 'button-text.link-next').click()
        time.sleep(3)
```

#### Step 3: Define Dictionaries for Scraping Data

```bash
    reference_dict = {
        "Name": "style__pro-title___2QwJy",
        "Size": "style__pack-size___2JQG7",
        "MRP": "style__discount-price___25Bya",
        "Price": "style__price-tag___cOxYc",
        "1mg URL": ["style__product-link___UB_67", "href"],
        "Ratings": "CardRatingDetail__weight-700___27w9q",
        "No. of Ratings": "CardRatingDetail__ratings-header___2yyQW",
    }

    values_dict = {
        "Name": [],
        "Size": [],
        "MRP": [],
        "Price": [],
        "1mg URL": [],
        "Ratings": [],
        "No. of Ratings": [],
    }

```

#### Step 4: Extract Values Using Defined Dictionary
```bash
    def extract_values(total_records, class_name, att=0):
        values = []
        if att == 0:
            for i in total_records:
                try:
                    values.append(i.find_element(By.CLASS_NAME, class_name).text)
                except:
                    values.append("NA")
        else:
            for i in total_records:
                try:
                    values.append(i.find_element(By.CLASS_NAME, class_name).get_attribute(att))
                except:
                    values.append("NA")
        return values

    for key, value in values_dict.items():
        if len(reference_dict[key]) != 2:
            value.extend(extract_values(parent_list, reference_dict[key]))
        else:
            value.extend(extract_values(parent_list, reference_dict[key][0], reference_dict[key][1]))

    product_df = pd.DataFrame.from_dict(values_dict)
```
#### Step 5: Scrape Information for Each Product (Opening every product link and scrapping data)

```bash
    remain_values = {
        "Name": [],
        "Brand Name": [],
        "Key Benefits": [],
        "Key Ingredients": [],
    }

    def get_element_text(by, value):
        try:
            return driver.find_element(by, value).text
        except NoSuchElementException:
            return " "

    for url in values_dict['1mg URL']:
        driver.get(url)

        key_ingredients = []
        key_benefits = []
        name_brand_added = False

        try:
            WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.CLASS_NAME, 'ProductTitle__product-title___3QMYH')))
            product_name = get_element_text(By.CLASS_NAME, 'ProductTitle__product-title___3QMYH')
            brand_name = get_element_text(By.CLASS_NAME, 'ProductTitle__marketer___7Wsj9')

            remain_values["Name"].append(product_name)
            remain_values["Brand Name"].append(brand_name)
            name_brand_added = True

            WebDriverWait(driver, 4).until(
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
                            key_ingredients.extend([child.text for child in sibling.find_elements(By.XPATH, ".//*")])
                        elif "benefits" in heading_text:
                            key_benefits.extend([child.text for child in sibling.find_elements(By.XPATH, ".//*")])

        except TimeoutException:
            print(f"Timed out waiting for elements on page: {url}")
            if not name_brand_added:
                remain_values["Name"].append("")
                remain_values["Brand Name"].append("")

        except NoSuchElementException as e:
            print(f"Element not found: {str(e)}")
            if not name_brand_added:
                remain_values["Name"].append("")
                remain_values["Brand Name"].append("")

        if not key_ingredients:
            prod_des = driver.find_element(By.CLASS_NAME, 'ProductDescription__description-content___A_qCZ').text
            pattern = re.compile(r'Key Ingredients?:\s*((?:.+\n?)+)(?=\n\n|Key Benefits:|Directions For Use:|Safety Information:|Indications:)')
            match = pattern.search(prod_des)
            if match:
                key_ingredients = match.group(1).strip().splitlines()
                remain_values["Key Ingredients"].append(key_ingredients)
            else:
                remain_values["Key Ingredients"].append([])
        else:
            remain_values["Key Ingredients"].append(key_ingredients)

        if not key_benefits:
            remain_values["Key Benefits"].append([])
        else:
            remain_values["Key Benefits"].append(key_benefits)

        time.sleep(2)

    driver.quit()
```
#### Step 6: Checking and Combining the Whole Data into a DataFrame for Cleaning 
```bash
    for i in remain_values.values():
        print(len(i))

    remaining_data = pd.DataFrame.from_dict(remain_values)
    combined_data = pd.concat([product_df, remaining_data], axis=1)

```

### 4. Data Cleaning

After scraping the data, it is essential to clean it to ensure accuracy and consistency. The following steps are performed for data cleaning:

#### Step 1: Handle Missing Values and Duplicate Records
```bash
    data_copy = combined_data.copy()

    data_copy.drop_duplicates(subset=["name", "size_of_the_bottle", "MRP_of_the_bottle", "price_of_the_bottle", "1mg_url", "brand_name", "rating", "number_of_rating"], inplace=True)
```
#### Step 2: Standardize Data Types
```bash
    data_copy['size_of_the_bottle'] = data_copy['size_of_the_bottle'].str.extract(r'(\d+\s*\w+)', expand=False)
    data_copy['price_of_the_bottle'] = data_copy['price_of_the_bottle'].str.extract(r'(\d+)').astype(float)
    data_copy['MRP_of_the_bottle'] = data_copy['MRP_of_the_bottle'].str.extract(r'(\d+)').astype(float)
    data_copy['MRP_of_the_bottle'].fillna(data_copy['price_of_the_bottle'], inplace=True)
    data_copy['rating'] = data_copy['rating'].replace("NA", 0).astype(float)
    data_copy['number_of_rating'] = data_copy['number_of_rating'].str.extract(r'(\d+)').fillna(0).astype(int)
```
#### Step 3: Save Cleaned Data to CSV
```bash
    data_copy.to_csv("Table2_scrapingData.csv", index=False)
    data_copy["name"].to_csv("Table1_scrapingData.csv", index=False)
```

### 5. Data Analysis

After scraping and cleaning the data, we proceeded to analyze it to extract meaningful insights. The primary focus of our analysis was to understand the landscape of homeopathic medicines available on the 1mg platform. Here are the key steps and techniques we used in our data analysis:

#### Descriptive Statistics:

- Price Analysis: We calculated the average, minimum, and maximum prices of medicines for each brand and benefit area.
- Rating Analysis: We analyzed the average ratings and the number of ratings for each product to identify the most popular and highly-rated medicines.
- Ingredient Analysis: We examined the frequency of key ingredients used in the medicines and their average costs.

#### Grouping and Aggregation:

- Benefit Area Analysis: We grouped the medicines based on their key benefits (e.g., hair, eye, joint, skin) to identify the number of medicines available in each category.
- Brand Specialization: We analyzed which brands specialize in specific benefit areas by looking at the concentration of their products in those categories.

#### Trend Analysis:

- We looked at the distribution of prices and ratings across different brands and benefit areas to identify trends and outliers.

Here, I'm including the document with the detailed insights we derived from our data analysis. 

[Detailed insights](https://docs.google.com/document/d/1MRDUmlni0seznXXl5nGlEIMxjaiIU5RIW4dprsrbKMo/edit?usp=sharing)

Additionally, here are some graphs that we plotted to give you more visual insights. These graphs complement the visual insights available in the dashboard and provide a deeper understanding of the data.

![Graphs]()

### 6. Dashboard Creation
To make our analysis accessible and user-friendly, we created an interactive dashboard using visualization tools. The dashboard provides a comprehensive view of the homeopathic medicine market on the 1mg platform. Key features of the dashboard include:
- Interactive Filters
- Visual Representations
- Detailed Tables
- Insights

Here is a screenshot of the dashboard:


![Dashboard](https://github.com/ghanshyamjadhav2125/AMD_Architects/blob/main/Dashboard/Dashboard.png)


The dashboard is designed to be an invaluable tool for stakeholders, allowing them to explore the data dynamically and make informed decisions.



### 7. Conclusion
Our project successfully demonstrates the process of scraping, cleaning, analyzing, and visualizing data from a dynamic website. By leveraging Selenium for web scraping, Pandas and NumPy for data processing, and interactive visualization tools for dashboard creation, we have created a comprehensive and insightful overview of the homeopathic medicine on the 1mg platform.

This project not only provides valuable insights in the homeopathic medicine industry but also showcases the power of data analysis and visualization in making data-driven decisions.

We hope our work will be a valuable resource for anyone looking to explore the homeopathic medicine market. Thank you for your interest in our project. We look forward to any feedback or questions you may have.
