# Setting up MariaDB container

### Process to set up MariaDB container using image from registry.redhat.io
(Used docker for building the container but same commands apply for podman)

```
docker login registry.redhat.io <username>
docker run -p 127.0.0.1:3307:3306 --name mymaria -e MYSQL_USER=user1 -e MYSQL_PASSWORD=mypa55 -e MYSQL_DATABASE=certs -e MYSQL_ROOT_PASSWORD=mypass -d registry.access.redhat.com/rhscl/mariadb-102-rhel7
```

### Running database inside the container
```
docker exec -it mymaria /bin/bash
mysql -uroot
```

### Accessing database from outside the container with MySQL
```
mysql -h 127.0.0.1 -P 3307 --protocol=TCP -u root -p
```