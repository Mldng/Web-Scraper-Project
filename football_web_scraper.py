from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time
import os

def get_data_ENG(url) -> pd:
    """
    Scrapes football match data from a given URL
    and returns it as a pandas DataFrame.

    This function opens the given URL in a Chrome WebDriver,
    then it locates and clicks on the 'All matches' button.
    It then extracts data for each match, including date,
    home team, score, and away team,
    and compiles this information into a pandas DataFrame.

    Args:
        url (str): The URL of the website to scrape for match data.

    Returns:
        pd.DataFrame: A DataFrame containing the scraped data with columns for date,
                      home team, score, and away team.

    Note:
        This function assumes that the webpage structure contains specific elements
        identifiable by given XPATHs and tags. Changes in the web page's structure may
        require updates to the locators used in this function.
    """

    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome()
    driver.get(url)

    # Find and click the 'All matches' button
    all_matches_btn = (driver.find_element(By.XPATH,
                                           '//label[@analytics-event="All matches"]')
                       )
    all_matches_btn.click()

    # Find all match elements
    matches = driver.find_elements(By.TAG_NAME,'tr')

    # Initialize lists to store match data
    dates = []
    home_teams = []
    scores = []
    away_teams = []

    # Iterate through each match and extract data
    for match in matches:
        date = match.find_element(By.XPATH,'./td[1]').text
        home_team = match.find_element(By.XPATH,'./td[2]').text
        score = match.find_element(By.XPATH,'./td[3]').text
        away_team = match.find_element(By.XPATH,'./td[4]').text

        dates.append(date)
        home_teams.append(home_team)
        scores.append(score)
        away_teams.append(away_team)

    # Quit the WebDriver session
    driver.quit()

    # Create a DataFrame from the extracted data
    df = pd.DataFrame({
        'dates': dates,
        'home_teams': home_teams,
        'scores': scores,
        'away_teams' : away_teams
    })
    return df

def get_data_dropdown(url,index) -> pd:
    """
    Scrapes football match data for a specific country from a given URL and
    returns it as a pandas DataFrame.

    This function opens the given URL in a Chrome WebDriver, clicks on the
    'All matches' button, and then selects a country from a dropdown menu based
    on the provided index. It extracts match data including dates, home teams,
    scores, and away teams for the selected country, and compiles this information
    into a pandas DataFrame.

    Args:
        url (str): The URL of the website to scrape for match data.
        index (int): The index of the country in the dropdown menu to select.

    Returns:
        pd.DataFrame: A DataFrame containing the scraped data with columns for
                      date, home team, score, and away team.

    Note:
        This function includes explicit time delays (using time.sleep()) to allow
        for dynamic content loading on the page. The webpage structure should contain
        specific elements identifiable by given XPATHs, IDs, and tags. Changes in the
        web page's structure may require updates to the locators used in this function.
    """

    print(f'Getting data for country {index}')

    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome()
    driver.get(url)

    # Find and click the 'All matches' button
    all_matches_btn = (driver.find_element(By.XPATH,
                                           '//label[@analytics-event="All matches"]')
                       )
    all_matches_btn.click()

    # Wait for dynamic content to load
    time.sleep(5)

    try:
        # Select a country from the dropdown menu
        dropdown = Select(driver.find_element(By.ID,'country'))
        dropdown.select_by_index(index)
    except NoSuchElementException:
        print("There is no element with that index")
        driver.quit()
        return pd.DataFrame()  # Return an empty DataFrame

    # Wait again for dynamic content to load after selection
    time.sleep(5)

    # Find all match elements
    matches = driver.find_elements(By.TAG_NAME,'tr')

    # Initialize lists to store match data
    dates = []
    home_teams = []
    scores = []
    away_teams = []

    # Iterate through each match and extract data
    for match in matches:
        date = match.find_element(By.XPATH,'./td[1]').text
        home_team = match.find_element(By.XPATH,'./td[2]').text
        score = match.find_element(By.XPATH,'./td[3]').text
        away_team = match.find_element(By.XPATH,'./td[4]').text

        dates.append(date)
        home_teams.append(home_team)
        scores.append(score)
        away_teams.append(away_team)

    # Quit the WebDriver session
    driver.quit()

    # Create a DataFrame from the extracted data
    df = pd.DataFrame({
        'dates': dates,
        'home_teams': home_teams,
        'scores': scores,
        'away_teams' : away_teams
    })
    return df

def save_csv(df, index):
    print(f'Saving data for country {index}')
    save_path = os.path.join(os.getcwd(),'csv')
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    save_name = f'{save_path}/football_data_{index}.csv'
    df.to_csv(save_name, index=False)
    print(f'finished saving data for country {index}')

def main():
    # Define the URL
    url = "https://www.adamchoi.co.uk/overs/detailed"
    country_index = 0  # Start from index 0

    while True:
        # Get data
        print(f"Scraping data for country index {country_index}...")
        df = get_data_dropdown(url, country_index)

        # Check if the DataFrame is empty (indicating no such index)
        if df.empty:
            print(f"No element with index {country_index}, stopping.")
            break

        # Save data to CSV
        print(f"Saving data for country index {country_index}...")
        save_csv(df, country_index)

        # Increment the index for the next iteration
        country_index += 1

    print("Data scraping and saving completed successfully")

if __name__ == "__main__":
    main()
