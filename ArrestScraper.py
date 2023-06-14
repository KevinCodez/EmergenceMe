from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import DataFormatter

def fetch_arrests():

    # Wheather or not program just started up
    isFirstRun = True

    # List of formatted arrests
    formatted_arrests = []

    # Launch Browser
    browser = webdriver.Firefox()

    try:
        # Timeout in 5 seconds if the page is not loaded
        browser.set_page_load_timeout(10)

        # Go to the dispatch log site
        browser.get("https://sheriff.washingtoncountyar.gov/res/DIntakeRoster.aspx")

        # Wait for site to load then store all "tr" elements in a "dispatches" list
        arrests = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'tr')))
    except:
        browser.close()
        print("Failed to load site in a timely manner")
        return "error_handled"

    # Remove the first element (table header) in the list
    arrests.pop(0)

    # Iterate and reformat the data to a list
    # Each dispatch is formatted and stored in the "formattedIncidents" tuple
    # ("Date | Time", "DESCRIPTION", "ADDRESS")
    # try:
    for i, arrest in enumerate(arrests):
        # individual arrest information
        arrest_info = arrest.find_elements(By.TAG_NAME, 'td')

        # Initialize / Reset data
        name = ""
        url = ""
        booking_date = ""
        booking_time = ""
        address = ""
        city = ""
        charges = []

        # Breaks up the data
        if len(arrest_info) == 7:

            # Extract name
            if arrest_info[0].text == "":
                name = "N/A"
            else:
                name = arrest_info[0].text

                if not isFirstRun and i >= 9:
                    break
                
                # Extract URL
                nested_element = arrest.find_elements(By.TAG_NAME, 'a')
                url = nested_element[0].get_attribute("href")

        # Launch a secondary browser
        second_browser = webdriver.Firefox()

        # try:
            # Timeout in 5 seconds if the page is not loaded
        second_browser.set_page_load_timeout(10)

        # Go to the dispatch log site
        second_browser.get(url)

        # Wait for site to load then store all "tr" elements in a "dispatches" list
        detainee_info = WebDriverWait(second_browser, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'tr')))
        address = detainee_info[0].find_element(By.CSS_SELECTOR, 'span#ContentPlaceHolder1_lbladdress').text
        city = detainee_info[0].find_element(By.CSS_SELECTOR, 'span#ContentPlaceHolder1_lblcityzip').text

        pad = 0
        if len(detainee_info[2].find_elements(By.CSS_SELECTOR, 'span#ContentPlaceHolder1_lblReleased')) > 0:
            pad = 1

        booking_date = detainee_info[9 + pad].find_element(By.CSS_SELECTOR, 'span#ContentPlaceHolder1_lblidate').text
        booking_time = detainee_info[10 + pad].find_element(By.CSS_SELECTOR, 'span#ContentPlaceHolder1_lblitime').text
        
        for i in range(17 + pad, len(detainee_info)):

            #Extract Charges
            nested_element = detainee_info[i].find_elements(By.TAG_NAME, 'td')
            charge = nested_element[0].text
            charges.append(charge)
        # except:
        #     second_browser.close()
        #     print("Failed to load detainee information")
        #     return "error_handled"

        arrest_data = []
        arrest_data.append(name)
        arrest_data.append(address)
        arrest_data.append(city)
        arrest_data.append(booking_date)
        arrest_data.append(booking_time)
        arrest_data.append(charges)
        arrest_data.append(url)

        second_browser.close()
        formatted_arrests.append(DataFormatter.format_arrest(arrest_data))

    browser.close()
    return formatted_arrests