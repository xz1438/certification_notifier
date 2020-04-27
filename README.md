# certification_notifier
This repo scrub the access.redhat.com and returns all current certifications and sends you an email 6 months before it expires

building the environment on RHEL8 :
- dnf install python3-pip
- python3 -m pip install pandas
- python3 -m pip install beautifulsoup4
- python3 -m pip install lxml
- python3 -m pip install secure-smtplib
- python3 -m pip install requests
