import datetime


# Formats and returns the data into an easy to understand list
def format_incident(incident):

    # Convert Date and time string to datetime objects
    # 05-08-2021 | 04:12:00
    incident_time = datetime.datetime.strptime(incident[0], '%m-%d-%Y | %H:%M:%S')
    date = incident_time.strftime("%m/%d/%Y")
    time = incident_time.strftime("%I:%M %p")
    if time[0] == '0':
        time = time[1:]
    description = incident[1]
    location = incident[2]
    formatted_incident = [date, time, description, location]
    return formatted_incident