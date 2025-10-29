import requests
import time, os, csv
import json, re, random
from urllib.parse import urlencode
from DrissionPage import ChromiumOptions
from DrissionPage import ChromiumPage
from DrissionPage.common import Keys
from lxml.html import fromstring


def browser_setup():
    browser = ChromiumPage()
    option = ChromiumOptions()
    option.headless()
    driver = browser.new_tab()
    return driver

def get_business_links(driver):
    page_start = 0
    items_per_page = 10
    
    while True:
        page = page_start * items_per_page
        params = {
            "find_desc": "Restaurants",
            "find_loc": "San Francisco, CA",
            "start": page,
            "dd_referrer": ""
        }
        page_url = "https://www.yelp.com/search?" + urlencode(params)
        print(f'[-> ] Getting Base URL : {page_url}')
        driver.get(page_url)
        time.sleep(random.uniform(1.5, 3.7))
        driver._wait_loaded(5)
        [driver.actions.key_down(k) or time.sleep(random.uniform(0.4, 1.5)) for k in [Keys.DOWN]* random.randint(50, 93)]
        soup = fromstring(driver.html)
        contaier = soup.xpath('//div[@data-testid="serp-ia-card"]//div[contains(@class,"businessName")]//a')
        next_page = soup.xpath('//button[contains(@class, "pagination-button") and @disabled]')
        if next_page:break
        existing_data_links = check_saved_links()
        for item in contaier:
            fresh_link = 'https://www.yelp.com' + item.get('href')
            if fresh_link in existing_data_links:continue
            else: save_category_links(fresh_link)
            
        page_start += 1

def check_saved_links():
    with open('yelp_business_data.txt', 'r', encoding='utf-8') as file:
        saved_links = [link.strip() for link in file.readlines()]
        return saved_links

def save_category_links(link):
    with open('yelp_business_data.txt', 'a', encoding='utf-8') as file:
        file.write(str(link) + '\n')

def read_urls():
    with open('yelp_business_data.txt','r',encoding='utf-8') as file:
        alread_save_links = [link.strip() for link in file if link.strip()]
        return alread_save_links
    
def scrape_yelp_page(driver, link):
    driver.get(link);
    driver._wait_loaded(3)
    soup = fromstring(driver.html)
    title_tag = soup.xpath('//div[contains(@class,"headingLight")]/h1')
    title = title_tag[0].text.strip() if title_tag else 'N/A'
    phone_tag = soup.xpath('//div[@class="y-css-8x4us"]//p[text()="Phone number"]/following-sibling::p')
    phone_number = phone_tag[0].text.strip() if phone_tag else 'N/A'
    site_tag = soup.xpath('//div[@class="y-css-8x4us"]//p[text()="Business website"]/following-sibling::p/a')
    business_site = site_tag[0].get('href').strip() if site_tag else 'Business Site Not Found'
    addres_tag = soup.xpath('//div[@class="y-css-8x4us"]//a[text()="Get Directions"]/../following-sibling::p')
    business_address = addres_tag[0].text_content().strip() if addres_tag else 'N/A'
    csv_row = [title, phone_number, business_site, business_address]
    save_to_csv(csv_row)
    # return {'Business Name':title,'Phone Number':phone_number,'Website':business_site,'Address':business_address,'URL':link}    

def save_to_csv(row):
    file_name = 'yelp_business_data.csv'
    with open(file_name, 'a',newline='',encoding='utf-8') as file:
       csv.writer(file).writerow(row)
    
    print(f'[!] Saved Data To CSV : ')


def main():
    open('yelp_business_data.txt', 'w', encoding='utf-8').close()
    driver = browser_setup()
    get_business_links(driver)
    links = read_urls()
    for link in links:
        scrape_yelp_page(driver, link)


if __name__ == '__main__':
    main()

