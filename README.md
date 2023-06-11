# EmergenceMe
A python script which sends the user a text message when the Fayetteville Police, Fire Department, or Central EMS are dispatched to a user-specified location.

This program periodically scrapes data from the Fayetteville Police dispatch logs using Selenium. The program then sends a text to specified users via the Twilio API with the corresponding information of the incident. All incident information is stored in a CSV file.

<img width="255" alt="Example of EmergenceMe" src="https://github.com/KevinCodez/EmergenceMe/assets/39411500/7ffa37e2-65f1-41aa-abe7-b889b1345769">

