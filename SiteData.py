from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

def get_site_data():
    # Launch and configure Browser
    browser = webdriver.Chrome()
    type(browser)

    # Set the implicit wait timeout
    browser.implicitly_wait(10)

    # Set the page load timeout
    browser.set_page_load_timeout(15)

    try:
        # Go to the dispatch log site
        browser.get("https://maps.fayetteville-ar.gov/DispatchLogs/")

        # Wait for site to load then store all "tr" elements in a "dispatches" list
        time.sleep(5)
        dispatches = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'tr')))

        # Remove the first element in the list
        dispatches.pop(0)

        # Will store Tuples of formatted information
        formattedIncidents = []

        # Iterate and reformat the data to a list
        # Each dispatch is formatted and stored in the "formattedIncidents" tuple
        # ("Date | Time", "DESCRIPTION", "ADDRESS")
        for dispatch in dispatches:
            # incident_info = individual incident information
            incident_info = dispatch.find_elements(By.TAG_NAME, 'td')

            # Initialize / Reset data
            incident_time = ""
            description = ""
            location = ""

            # Breaks up the data
            if len(incident_info) == 3:
                for i in range(3):
                    # Set Date and time
                    if i == 0:
                        if incident_info[i].text == "":
                            incident_time = "N/A"
                        else:
                            incident_time = incident_info[i].text

                    # Set information
                    if i == 1:
                        if incident_info[i].text == "":
                            description = "N/A"
                        else:
                            description = incident_info[i].text

                    # Set Location
                    if i == 2:
                        if incident_info[i].text == "":
                            location = "N/A"
                        else:
                            location = incident_info[i].text.upper()
            else:
                browser.close()
                return "error"

            # Appends the set info to the list
            formattedIncidents.append((incident_time, description, location))

        browser.close()
        return formattedIncidents
    except:
        print("Failed to load site in a timely manner")
        browser.close()
        return "error"