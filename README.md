# software-tracker

## Set up software tracker database and web server in Kubernetes

1. Setup mysql database, see [mysql](mysql/README.md)
2. Create docker image for web application, see [docker](docker/README.md)
3. Create dns, see [dns](dns/README.md):  
   - dev [paso.tol-dev.sanger.ac.uk](http://paso.tol-dev.sanger.ac.uk/)
   - prod [paso.tol.sanger.ac.uk](http://paso.tol.sanger.ac.uk/)
4. Check Helm values with correct details, especially database details, you may create a new values file.
   - [dev](software-tracker-dev-values.yaml)
   - [prod](software-tracker-prod-values.yaml)
5. Helm install web application
    - [dev](software-tracker-dev-helm-readme.md)
    - [prod](software-tracker-prod-helm-readme.md)

## Query the database
Connect to MySQL host:
  - dev:  mysql -h software-tracker-test-db.internal.sanger.ac.uk -P 3350 -u tol -p software_tracker
  - prod: mysql -h software-tracker-prod-db.internal.sanger.ac.uk -P 3351 -u tol -p software_tracker
```
SELECT * FROM logging_event;
```

## Query from the simple web interface
- dev [paso.tol-dev.sanger.ac.uk](http://paso.tol-dev.sanger.ac.uk/)
- prod [paso.tol.sanger.ac.uk](http://paso.tol.sanger.ac.uk/)

## Query from a script

```shell
./log-query.sh gq2 'quay.io-biocontainers-samtools-1.15--h1170115_1-sha256:d310e040333c77b6e56999f8e4e98f9e615bc398f9bffad4036837bceaeef3db.sif' /nfs/users/nfs_g/gq2 samtool 
```
