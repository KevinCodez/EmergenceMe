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

def format_arrest(incident):
    # incident = [name, address, city, booking_date, booking_time, charges[], url]

    # Format the name
    # Split the name into last name and first name
    last_name, first_name = incident[0].split(", ")

    # Remove leading/trailing spaces
    last_name = last_name.strip()
    first_name = first_name.strip()

    # Construct the new name in "firstname lastname" format
    incident[0] = f"{first_name} {last_name}"

    # Format the time
    # Split the time into hours and minutes
    hours, minutes = map(int, incident[4].split(':'))

    # Determine the meridiem (AM or PM)
    meridiem = 'AM' if hours < 12 else 'PM'

    # Convert hours to 12-hour format
    hours = hours % 12 if hours % 12 != 0 else 12

    # Construct the new time in 12-hour format
    incident[4] = f"{hours}:{minutes:02d} {meridiem}"

    return incident