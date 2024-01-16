import csv
import time
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
import random

class crawledArticle():
    def __init__(self, title, price):
        self.title = title
        self.price = price

class Bot:
    def get_browser(self):
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Mozilla/5.0 (iPad; CPU OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0"
        ]

        options = ChromeOptions()
        # Set a random user-agent from the list
        options.add_argument(f'user-agent={random.choice(user_agents)}')
        options.headless = False
        options.add_experimental_option("detach", True)

        browser = Chrome(options=options)
        browser.maximize_window()
        return browser

    def article(self, name):
        count = 1 #number of article
        page = 1 #number of pages to be crawled
        page_increment = 10 #how many count per pages
        max_retrieves = 100 #maximum number to retrieve
        info_list = []

        url = f"https://www.amazon.co.jp/s?k={name}&page={page}"

        options = ChromeOptions()
        options.headless = False
        options.add_experimental_option("detach", True)

        browser = Chrome(options=options) #don't close web browser when we quit Bot
        browser.maximize_window() #to keep html unchange so we can get same stuff
        browser.get(url)
        browser.set_page_load_timeout(10) #wait 10 seconds

        while True:
            try:
                if page_increment * page > max_retrieves:
                    break
                if count > page_increment:
                    count = 1
                    page += 1

                #Get title
                XPath_title = (f'//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[{count}]/div/div/div/div/span/div/div/div[2]/div[1]/h2/a/span')
                title = browser.find_element(By.XPATH,XPath_title)
                title_text = title.get_attribute("innerHTML").splitlines()[0]
                title.click()
                time.sleep(10)

                XPath_price = '//*[@id="corePrice_feature_div"]'
                price = browser.find_element(By.XPATH,XPath_price)
                price_text = price.get_attribute("innerHTML")

                url = f"https://www.amazon.co.jp/s?k={name}&page={page}"
                browser.get(url)
                browser.set_page_load_timeout(10) #wait 10 seconds

                info = crawledArticle(title_text,price_text)
                info_list.append(info)

                count += 1
            except Exception as e:
                print(f"Exception {e}")
                count += 1

                if page_increment * page > max_retrieves:
                    break
                if count > page_increment:
                    count = 1
                    page += 1

                url = f"https://www.amazon.co.jp/s?k={name}&page={page}"
                browser.get(url)
                browser.set_page_load_timeout(10) #wait 10 seconds

        browser.quit()

        return info_list

fetcher = Bot()

with open('result.csv', 'w', newline='', encoding='utf-8') as csvfile:
    article_writer = (csv.writer(csvfile,
                                 delimiter=';',
                                 quotechar='"',
                                 quoting=csv.QUOTE_MINIMAL)
    )
    for article in fetcher.article('dyson'):
        article_writer.writerow([article.title, article.price])
