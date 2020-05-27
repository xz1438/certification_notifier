# certification_notifier
This repo scrub the access.redhat.com and returns all current certifications and sends you an email 6 months before it expires

Building the environment on RHEL8 :
- dnf install python3-pip
- subscription-manager repos --enable='codeready-builder-for-rhel-8-x86_64-rpms'
- dnf -y install gpgme-devel
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
- podman pull rhel8/python-38
- git clone https://github.com/amalivert/certification_notifier.git
- git checkout dev
- mkdir /root/build
- cp -Rf /root/certification_notifier/ /root/build/
- cd /root/build/
- podman build certification_notifier
- podman images
- podman tag <IMAGE ID> cert_notifier
- podman run -i -t localhost/cert_notifier /bin/bash

