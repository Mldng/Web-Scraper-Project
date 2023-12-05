from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By

def get_data(url) -> list:
    browser_options = ChromeOptions()
    browser_options.headless = True

    driver = Chrome(options=browser_options)
    driver.get(url)

    driver.quit()

def main():
    data = get_data(url)

if __name__ == '__main__':
    main()
