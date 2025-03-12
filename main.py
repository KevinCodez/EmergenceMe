from DispatchScraper import fetch_incidents
from ArrestScraper import fetch_arrests
import DataFormatter
import data.Config as Config
import csv
import time
from twilio.rest import Client

twilioClient = Client(Config.myTwilioSID, Config.myAuthToken)


def check_for_new_dispatches():

    # Fetch site data
    try:
        incidents = fetch_incidents()
    except:
        print("Error: Logs could not be loaded")
        return 1

    # Check for error
    if incidents == "error_handled":
        return 1

    previous_times = []
    previous_dates = []

    # Reads CSV file and
    with open('data/Dispatches.csv') as readFile:
        csvReader = csv.reader(readFile, skipinitialspace=True)
        for row in csvReader:
            previous_times.append(row[1])
            previous_dates.append(row[0])

    # Removes the quotes from the previous_times values
    previous_times = [i.replace("'", "") for i in previous_times]

    with open('data/Dispatches.csv', 'a', newline='') as writeFile:

        csvWriter = csv.writer(writeFile)

        monitored_streets = Config.monitored_streets

        # Checks each incident for a matching street name
        for incident in incidents:
            if checkMatch(monitored_streets, incident[2]): # Check if incident street name matches the monitored_streets
                
                for i in range(len(previous_times) + 1): # Check if information is already in CSV file
                    if i == len(previous_times):
                        # The incident is new. Save info and send text
                        
                        # Incident is new
                        formatted_incident = DataFormatter.format_incident(incident)

                        # Add incident to CSV File
                        writeFile.writelines(str(formatted_incident) + '\n')

                        # Print information to console
                        print(f"\n** {formatted_incident[2]} **")
                        print(formatted_incident[0])
                        print(formatted_incident[1])
                        print(formatted_incident[3] + '\n')

                        # Send text message
                        message = f"** {formatted_incident[2]} **\n\n{formatted_incident[0]}\n{formatted_incident[1]}\n\n{formatted_incident[3]}"
                    
                        for cellNumber in Config.numbersToText:
                            sendTextMessage(message, cellNumber)
                            
                        print("\n")
                        break
                    elif DataFormatter.format_incident(incident)[1] == previous_times[i]:
                        prev_date = previous_dates[i][2:-1]
                        if DataFormatter.format_incident(incident)[0] == prev_date:
                            # Date and time and street name match, this incident has been alerted already
                            break

def check_for_new_arrests():
    # arrest = [name, address, city, booking_date, booking_time, charges, url]

    arrests = fetch_arrests()

    if arrests == "error":
        return 1

    previous_times = []
    previous_dates = []

    # Reads CSV file and
    with open('data/Arrests.csv') as readFile:
        csvReader = csv.reader(readFile, skipinitialspace=True)
        for row in csvReader:
            if len(row) > 4:  # Check if the row has at least 5 elements
                previous_dates.append(row[3])
            else:
                previous_dates.append('')  # If the row is empty or has fewer elements, add an empty string for date

            if len(row) > 5:  # Check if the row has at least 6 elements
                previous_times.append(row[4])
            else:
                previous_times.append('')  # If the row is empty or has fewer elements, add an empty string for time

    previous_dates = [i.replace("'", "") for i in previous_dates]
    previous_times = [i.replace("'", "") for i in previous_times]

    with open('data/Arrests.csv', 'a', newline='') as writeFile:

        monitored_streets = Config.monitored_streets

        # Checks each incident for a matching street name
        for arrest in arrests:
            if checkMatch(monitored_streets, arrest[1]): # Check if arrest address matches any monitored_streets
                for i in range(len(previous_times) + 1): # Check if information is already in CSV file
                    if i == len(previous_times):

                        # The incident is new. Save info and send text
                        writeFile.writelines('"' + '", "'.join(map(str, arrest)) + '"\n')
                        
                        # Create message
                        print('\n')
                        s1 = f"** Neighbor Arrest **\n\n{arrest[0]}\n{arrest[1]}\n{arrest[2]}\n\n"
                        s2 = '\n'.join(arrest[5])
                        s3 = f"{arrest[6]}"
                        message = s1 + s2 + s3
                        print(message + '\n')

                        # Send text messages
                        for cellNumber in Config.numbersToText:
                            sendTextMessage(message, cellNumber)

                    elif arrest[4] == previous_times[i]:
                        if arrest[3] == previous_dates[i]:
                            # Date and time and street name match, this incident has been alerted already
                            break


def checkMatch(usersStreets, incidentLocation):
    for street in usersStreets:
        if street in incidentLocation:
            return True
    return False

def sendTextMessage(message, cellNumber):
    twilioClient.messages.create(body=message, from_=Config.myTwilioNumber, to=cellNumber)
    print(f"Text sent to {cellNumber}")
    time.sleep(3)

while True:
    check_for_new_dispatches()
    print("Finished checking dispatch logs")
    check_for_new_arrests()
    print("Finished checking arrest logs")
    print("Starting 30 minute timer\n")
    time.sleep(1800)

    check_for_new_dispatches()
    print("Finished checking dispatch logs")
    print("Starting 30 minute timer\n")
    time.sleep(1800)