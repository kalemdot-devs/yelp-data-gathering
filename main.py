import requests
import time, os, csv
import json, re, random
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
        page_url = f'https://www.yelp.com/search?find_desc=Restaurants&find_loc=San+Francisco%2C+CA&start={page}&dd_referrer='
        print(f'[-> ] Getting Base URL : {page_url}')
        driver.get(page_url)
        time.sleep(random.uniform(1.5, 3.7))
        driver._wait_loaded(5)
        [driver.actions.key_down(k) or time.sleep(random.uniform(0.4, 1.5)) for k in [Keys.DOWN]* random.randint(50, 93)]
        soup = fromstring(driver.html)
        contaier = soup.xpath('//div[@data-testid="serp-ia-card"]//div[contains(@class,"businessName")]//a')
        next_page = soup.xpath('//button[contains(@class, "pagination-button") and @disabled]')
        if next_page:break
        for item in contaier:
            href_link = 'https://www.yelp.com' + item.get('href')
            if 'biz' in href_link:
                with open('yelp_links.txt', 'a', encoding='utf-8') as file:
                    file.write(href_link + '\n')
        page_start += 1


def read_urls():
    with open('yelp_links.txt','r',encoding='utf-8') as x:
        return [i.strip() for i in x if i.strip()]

def scrape_yelp_page(driver):
    try:
        driver.get(u);
        p._wait_loaded(3)
        s=fromstring(p.html)
        t=s.xpath('//div[contains(@class,"headingLight")]/h1')
        n=t[0].text.strip() if t else 'N/A'
        ph=s.xpath('//div[@class="y-css-8x4us"]//p[text()="Phone number"]/following-sibling::p')
        phn=ph[0].text.strip() if ph else 'N/A'
        w=s.xpath('//div[@class="y-css-8x4us"]//p[text()="Business website"]/following-sibling::p/a')
        ws=w[0].get('href').strip() if w else 'N/A'
        a=s.xpath('//div[@class="y-css-8x4us"]//a[text()="Get Directions"]/../following-sibling::p')
        ad=a[0].text_content().strip() if a else 'N/A'
        return {'Business Name':n,'Phone Number':phn,'Website':ws,'Address':ad,'URL':u}
    except Exception as e:
        print(f"Error scraping {u}:{e}")
        return {'Business Name':'Error','Phone Number':'Error','Website':'Error','Address':'Error','URL':u}

def save_to_csv(d,f='yelp_data.csv'):
    if not d:return
    k=d[0].keys()
    with open(f,'w',newline='',encoding='utf-8') as x:
        w=csv.DictWriter(x,fieldnames=k)
        w.writeheader();w.writerows(d)
    print(f"Saved to {f}")


def main():
    driver = browser_setup()
    get_business_links(driver)


if __name__ == '__main__':
    main()

