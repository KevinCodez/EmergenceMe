# EmergenceMe
A python script which sends the user a text message when the Fayetteville Police, Fire Department, or Central EMS are dispatched to a user-specified location.

This program periodically scrapes data from the Fayetteville Police dispatch logs. The program then sends an email the users' cell phone gateway which then texts the user corresponding information of the incident. All incident information is stored in a CSV file. This program uses the "ezgmail" package as well as selenium (because the logging website is dynamic). Some google setup is required (see "ezgmail" documentation).

![IMG_DB3B2F7DF121-1](https://user-images.githubusercontent.com/39411500/117749412-5b226d80-b1d7-11eb-94c3-c7c57d55f304.jpeg)
