import SiteData
import formatter
import csv
import time
from twilio.rest import Client

myTwilioSID = '**********'
myAuthToken = '************'
myTwilioNumber = '+**********'
myCellPhone = '+**********'
twilioClient = Client(myTwilioSID, myAuthToken)


def check_for_new_records():

    # Fetch site data
    incidents = SiteData.get_site_data()

    # Check for error
    if incidents == "error":
        print("Error: Site data could not be loaded")
        return 1

    previous_times = []

    # Reads CSV file and
    with open('records.csv') as readFile:
        csvReader = csv.reader(readFile, skipinitialspace=True)
        for row in csvReader:
            previous_times.append(row[1])

    # Removes the quotes from the previous_times values
    previous_times = [i.replace("'", "") for i in previous_times]

    with open('records.csv', 'a', newline='') as writeFile:

        csvWriter = csv.writer(writeFile)

        street_query = "MLK"

        # Checks each incident for a matching street name
        for incident in incidents:
            # Check if incident street name matches the street_query
            if street_query in incident[2]:
                # Check if information is already in CSV file
                for i in range(len(previous_times) + 1):
                    if i == len(previous_times):
                        # Incident is new
                        formatted_incident = formatter.format_incident(incident)
                        # Add incident to CSV File
                        writeFile.writelines(str(formatted_incident) + '\n')

                        # Send text message
                        message = f"-\n\n** {formatted_incident[2]} **\n\n{formatted_incident[0]}\n{formatted_incident[1]}\n\n{formatted_incident[3]}"
                        twilioClient.messages.create(body=message, from_=myTwilioNumber, to=myCellPhone)
                        # print("Message sent")

                        # Print information to console
                        print(f"** {formatted_incident[2]} **")
                        print(formatted_incident[0])
                        print(formatted_incident[1])
                        print(formatted_incident[3] + '\n')

                        # Avoid spam / getting flagged
                        time.sleep(20)
                        break
                    elif formatter.format_incident(incident)[1] == previous_times[i]:
                        break


while True:
    check_for_new_records()
    print("Starting 30 minute timer")
    time.sleep(1600)
