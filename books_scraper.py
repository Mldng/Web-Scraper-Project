from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By

def get_data(url,category="Home") -> list:
    browser_options = ChromeOptions()
    browser_options.headless = True

    driver = Chrome(options=browser_options)
    driver.get(url)
    element = driver.find_element(By.LINK_TEXT,category)
    element.click

    books = driver.find_elements(By.CSS_SELECTOR,".product_pod")
    data = []
    for book in books:
        title = book.find_element(By.CSS_SELECTOR,"h3 > a")
        price = book.find_element(By.CSS_SELECTOR,".price_color")
        stock = book.find_element(By.CSS_SELECTOR,".instock.availability")

        book_item ={
            'title':title.get_attribute('title'),
            'price':price.text,
            'stock':stock.text
        }
        data.append(book_item)

    driver.quit()
    return data

def main(url="https://books.toscrape.com/"):
    data = get_data(url)
    print(data)

if __name__ == '__main__':
    main()
