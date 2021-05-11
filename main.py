import SiteData
import formatter
import csv
import time
import ezgmail


def check_for_new_records():

    # Fetch site data
    incidents = SiteData.get_site_data()

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

        street_query = "TULL"

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
                        message = f"/\n\n** {formatted_incident[2]} **\n\n{formatted_incident[0]}\n{formatted_incident[1]}\n\n{formatted_incident[3]}"
                        ezgmail.send(recipient='NUMBER@GATEWAY.net', subject='EmergenceMe', body=message)

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
