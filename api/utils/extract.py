import string
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import re
import time
from dotenv import load_dotenv
import os

load_dotenv()

letters = string.ascii_uppercase

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

def get_elements_of_letter(url):
    r = requests.get(url, headers=headers)
    letter_soup = BeautifulSoup(r.text, 'html.parser')
    total_elements = letter_soup.find(class_='latest-updates-results-header-summary-total')
    total_elements = total_elements.text.replace(" ", "")
    total_elements = int(total_elements.replace("resultsfound", ""))
    return total_elements

def get_urls(num, link):
    output_urls = set()
    for i in tqdm(range(1, num + 1, 50)):
        url_to_check = f'{link}?offset={i}&limit=50'
        response = requests.get(url_to_check, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        url_title_links = soup.find_all(class_="search-results-product-info-title-link emc-link")
        for j in url_title_links:
            if any(keyword in j.text for keyword in ["ablet", "apsule", "ozenge"]):
                href = 'https://www.medicines.org.uk/' + j.get('href')
                output_urls.add(href)
                
        time.sleep(1)
                
    return output_urls

def remove_html_tags(text):
    if isinstance(text, str):
        return re.sub(r'<[^>]+>', '', text)
    return text

def scrape_variable(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    #AGRESSIVE: options.setPageLoadStrategy(PageLoadStrategy.NONE); // https://www.skptricks.com/2018/08/timed-out-receiving-message-from-renderer-selenium.html
    chrome_options.add_argument("start-maximized");
    chrome_options.add_argument("enable-automation");
    chrome_options.add_argument("--no-sandbox");
    chrome_options.add_argument("--disable-dev-shm-usage"); 
    chrome_options.add_argument("--disable-browser-side-navigation"); 
    chrome_options.add_argument("--disable-gpu"); 
    chrome_options.add_argument("--disable-infobars"); 
    
    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(30)
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
    })
    driver.execute_cdp_cmd('Network.enable', {})

    try:
        driver.get(url)
        driver.execute_cdp_cmd('Network.setExtraHTTPHeaders', {
            'headers': {
                'Accept-Language': 'en-US,en;q=0.9',
            }
        })

        title = driver.title
        clean_title = title.split(' -')[0]

        # Active Ingredient
        active_ingredient = "N/A"
        try:
            active_ingredient_element = driver.find_element(By.XPATH, '/html/body/div[3]/section[2]/div/div[2]/div[1]/div[1]/div/a')
            active_ingredient = active_ingredient_element.text
        except:
            pass
        
        # Medicine Description
        description = "N/A"
        try:
            # Execute JavaScript to obtain the variable 'allDetails'
            all_details = driver.execute_script("return allDetails[2].childNodes[2].innerHTML;")
            
            description_pattern = r"<p>(.*?)</p>"
            if all_details:
                description = re.sub(description_pattern, r"\1", all_details)
        except:
            pass
        
        # Company name
        company = "N/A"
        try:
            company_element = driver.find_element(By.XPATH, '/html/body/div[3]/section[2]/div/div[2]/div[1]/div[2]/div/span')
            company = company_element.text
        except:
            pass

        return clean_title, active_ingredient, description, company

    finally:
        driver.quit()

urls_dict = {letter: [] for letter in letters}

for letter in letters:
    letter_url = f'{os.getenv('MEDICINE_URL_ENDPOINT')}'
    num_elements = get_elements_of_letter(letter_url)
    urls = get_urls(num=num_elements, link=letter_url)
    
    urls_dict[letter].extend(urls)

urls_list = [url for sublist in urls_dict.values() for url in sublist]

results = []

for url in tqdm(urls_list):
    title, active_ingredient, description, company = scrape_variable(url)
    results.append({
        "Page Title": title,
        "Active Ingredient": active_ingredient,
        "Description": description,
        "Company": company
    })
    
    time.sleep(1)

results_df = pd.DataFrame(results)
results_df['Description'] = results_df['Description'].apply(remove_html_tags)

results_df.to_csv("medicine_data.csv", index=False)