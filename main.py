from DispatchScraper import fetch_incidents
from ArrestScraper import fetch_arrests
import DataFormatter
import data.UserSecrets as UserSecrets
import csv
import time
from twilio.rest import Client

twilioClient = Client(UserSecrets.myTwilioSID, UserSecrets.myAuthToken)


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
    with open('Logs.csv') as readFile:
        csvReader = csv.reader(readFile, skipinitialspace=True)
        for row in csvReader:
            previous_times.append(row[1])
            previous_dates.append(row[0])

    # Removes the quotes from the previous_times values
    previous_times = [i.replace("'", "") for i in previous_times]

    with open('Logs.csv', 'a', newline='') as writeFile:

        csvWriter = csv.writer(writeFile)

        monitored_streets = UserSecrets.monitored_streets

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
                    
                        for cellNumber in UserSecrets.numbersToText:
                            sendTextMessage(message, cellNumber)
                            
                        print("\n")
                        break
                    elif DataFormatter.format_incident(incident)[1] == previous_times[i]:
                        prev_date = previous_dates[i][2:-1]
                        if DataFormatter.format_incident(incident)[0] == prev_date:
                            # Date and time and street name match, this incident has been alerted already
                            break

def check_for_new_arrests():
    arrests = fetch_arrests()

    if arrests == "error":
        return 1
    
    

def checkMatch(usersStreets, incidentLocation):
    for street in usersStreets:
        if street in incidentLocation:
            return True
    return False

def sendTextMessage(message, cellNumber):
    twilioClient.messages.create(body=message, from_=UserSecrets.myTwilioNumber, to=cellNumber)
    print(f"Text sent to {cellNumber}")
    time.sleep(3)

while True:
    # check_for_new_dispatches()
    check_for_new_arrests()
    print("Starting 30 minute timer")
    time.sleep(1600)
