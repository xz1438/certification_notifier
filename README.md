# certification_notifier
This repo scrub the access.redhat.com and returns all current certifications and sends you an email 6 months before it expires

Building the environment on RHEL8 :
- dnf install python3-pip
- python3 -m pip install pandas
- python3 -m pip install beautifulsoup4
- python3 -m pip install lxml
- python3 -m pip install secure-smtplib
- python3 -m pip install requests
- python3 -m pip freeze > requirements.txt
- python3 -m pip install -r requirements.txt
- python3 rh_cert_notify.py

Building Container:
- dnf -y install podman
- podman login registry.redhat.io < use Red Hat account credentials >
- dnf -y install buildah
- podman pull rhel8/python-38
- 
