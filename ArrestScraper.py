from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import DataFormatter

def fetch_arrests():

    # Stores tuples of formatted information
    formattedArrests = []

    # Read in last known arrest
    lastKnownArrest = ""
    with open('data/LastKnownArrest.txt') as file:
        lastKnownArrest = file.readline()

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

    # Write name of latest arrested person
    latest_arrest_name = arrests[0].find_elements(By.TAG_NAME, 'td')[0].text
    # with open("data/LastKnownArrest.txt", "w") as file:
    #     file.write(latest_arrest_name)

    # Iterate and reformat the data to a list
    # Each dispatch is formatted and stored in the "formattedIncidents" tuple
    # ("Date | Time", "DESCRIPTION", "ADDRESS")
    # try:
    for arrest in arrests:
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

                if name == lastKnownArrest:
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
        formatted_arrest = DataFormatter.format_arrest(arrest_data)
        for data in arrest_data:
            print(data)
        print("\n")
        # Appends the set info to the list
        # formattedArrests.append((incident_time, description, location))

    browser.close()
    return "test"
    # except:
    #     browser.close()
    #     print("Some unknown problem occured in LogsSiteData.py")
    #     return "error_handled"