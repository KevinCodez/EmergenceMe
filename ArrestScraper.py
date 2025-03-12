from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import DataFormatter

# Wheather or not program just started up
isNotFirstRun = False

def fetch_arrests():

    global isNotFirstRun

    # List of formatted arrests
    formatted_arrests = []

    # Configure Firefox options for headless mode
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")

    # Launch Firefox in headless mode
    browser = webdriver.Firefox(options=options)

    try:
        # Timeout in 5 seconds if the page is not loaded
        browser.set_page_load_timeout(10)

        # Go to the dispatch log site
        browser.get("https://www.washcosoar.gov/res/DetaineeIntakeRoster.aspx")

        # Wait for site to load then store all "tr" elements in a "dispatches" list
        arrests = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'tbody')))
        arrests = arrests.find_elements(By.TAG_NAME, 'tr')[1:]
    except:
        browser.close()
        print("Failed to load intake site in a timely manner")
        return "error"
    
    try:
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
            if len(arrest_info) == 8:

                # Extract name
                if arrest_info[0].text == "":
                    name = "N/A"
                else:
                    name = arrest_info[0].text

                    if isNotFirstRun and i >= 5:
                        break
                    
                    # Extract URL
                    nested_element = arrest.find_elements(By.TAG_NAME, 'a')
                    url = nested_element[0].get_attribute("href")
            try:
                # Launch a secondary browser
                second_browser = webdriver.Firefox(options=options)

                second_browser.set_page_load_timeout(10)

                # Go to the dispatch log site
                second_browser.get(url)

                # Wait for site to load then store all "tr" elements in a "dispatches" list
                detainee_info = WebDriverWait(second_browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div#SiteContentPlaceHolder_Results')))
            except Exception as e:
                second_browser.close()
                print("An error occured when attempting to open the second browser")
                print(e)
                return "error"
            
            address = detainee_info.find_element(By.CSS_SELECTOR, 'span#SiteContentPlaceHolder_lbladdress').text
            city = detainee_info.find_element(By.CSS_SELECTOR, 'span#SiteContentPlaceHolder_lblcityzip').text
            booking_datetime = detainee_info.find_element(By.CSS_SELECTOR, 'span#SiteContentPlaceHolder_lblidate').text
            booking_date, booking_time = booking_datetime.split(' ')
            
            charge_table = detainee_info.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')[1:]
            for charge_row in charge_table:
                # Extract Charge description
                charge_description = charge_row.find_element(By.TAG_NAME, 'td')
                charges.append(charge_description.text)

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
    except Exception as e:
        browser.close()
        print("Some issue occured in ArrestScrapper.py")
        print(e)
        return "error"

    browser.close()
    isNotFirstRun = True
    return formatted_arrests