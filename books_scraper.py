from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By

def get_data(url,category="Home") -> list:
    """
    Scrapes data from a web page for items in a specified category.

    This function initializes a headless Chrome WebDriver to navigate to the provided URL.
    It then locates and clicks on a link matching the given category. After navigating
    to the category page, the function finds all items matching the 'product_pod' CSS selector.
    For each item, it extracts the title, price, and stock availability.

    Args:
        url (str): The URL of the website to scrape.
        category (str, optional): The category of items to scrape. Defaults to 'Home'.

    Returns:
        list: A list of dictionaries, where each dictionary contains details of a book,
              including its title, price, and stock availability.

    Note:
        The function assumes the structure of the web page matches certain CSS selectors.
        Changes in the web page's structure may require updates to the CSS selectors used.
    """

    # Set up browser options for Chrome
    browser_options = ChromeOptions()
    browser_options.headless = True # Enable headless mode for background operation

    # Initialize a Chrome WebDriver with the specified options
    driver = Chrome(options=browser_options)
    driver.get(url)

    # Find and click on the link with the text matching the specified category
    element = driver.find_element(By.LINK_TEXT,category)
    element.click

    # Find all elements matching the CSS selector for 'product_pod'
    books = driver.find_elements(By.CSS_SELECTOR,".product_pod")
    data = []

    # Iterate through each book element found
    for book in books:
        # Extract title, price, and stock information from each book
        title = book.find_element(By.CSS_SELECTOR,"h3 > a")
        price = book.find_element(By.CSS_SELECTOR,".price_color")
        stock = book.find_element(By.CSS_SELECTOR,".instock.availability")

        # Construct a dictionary for each book with its details
        book_item ={
            'title':title.get_attribute('title'),
            'price':price.text,
            'stock':stock.text
        }
        data.append(book_item)

    # Close the browser once data collection is complete
    driver.quit()
    return data

def main(url="https://books.toscrape.com/"):
    data = get_data(url)
    print(data)

if __name__ == '__main__':
    main()
