# certification_notifier
This repo scrub the access.redhat.com and returns all current certifications and sends you an email 6 months before it expires

building the environment on RHEL8 :
- dnf install python3-pip
- python3 -m pip freeze > requirements.txt
- python3 -m pip install -r requirements.txt
- python3 rh_cert_notify.py

