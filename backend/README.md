# Setting up MariaDB container

### Process to set up MariaDB container using image from registry.redhat.io
(Same commands apply for docker; might need to run podman with sudo)

Database container info (can be whatever):
- Container name: mymaria
- Username = user1
- Password = mypa55
- Database = certs
- Root PW = mypass

```
sudo podman login registry.redhat.io <username>
sudo podman run -p 127.0.0.1:3307:3306 --name mymaria -e MYSQL_USER=user1 -e MYSQL_PASSWORD=mypa55 -e MYSQL_DATABASE=certs -e MYSQL_ROOT_PASSWORD=mypass -d registry.access.redhat.com/rhscl/mariadb-102-rhel7
```

### Obtaining database container IP Address
```
sudo podman inspect mymaria | grep IPAddress
```

### Accessing the MySQL Server inside the container
```
sudo podman exec -it mymaria /bin/bash
mysql -uroot
```

### Accessing database from host machine with MySQL
(Different IP address from Container IP)
```
mysql -h 127.0.0.1 -P 3307 --protocol=TCP -u root -p
```