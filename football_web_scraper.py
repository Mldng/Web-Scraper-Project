from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
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
    print(f'Getting data for country {index}')

    driver = webdriver.Chrome()
    driver.get(url)

    all_matches_btn = (driver.find_element(By.XPATH,
                                           '//label[@analytics-event="All matches"]')
                       )
    all_matches_btn.click()

    time.sleep(5)

    dropdown = Select(driver.find_element(By.ID,'country'))
    dropdown.select_by_index(index)

    time.sleep(5)

    matches = driver.find_elements(By.TAG_NAME,'tr')

    dates = []
    home_teams = []
    scores = []
    away_teams = []

    for match in matches:
        date = match.find_element(By.XPATH,'./td[1]').text
        home_team = match.find_element(By.XPATH,'./td[2]').text
        score = match.find_element(By.XPATH,'./td[3]').text
        away_team = match.find_element(By.XPATH,'./td[4]').text

        dates.append(date)
        home_teams.append(home_team)
        scores.append(score)
        away_teams.append(away_team)
    driver.quit()
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
    save_name = f'football_data_{index}.csv'
    df.to_csv(save_name, index=False)
    print(f'finished saving data for country {index}')
