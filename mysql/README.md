# BITNAMI MYSQL STACK HELM CHARTS

## Links
Helm: https://bitnami.com/stack/mysql/helm  
Helm Source: https://github.com/bitnami/charts/tree/master/bitnami/mysql/#installing-the-chart  

Docker: https://hub.docker.com/r/bitnami/mysql  
Docker Source: https://github.com/bitnami/bitnami-docker-mysql

## Add Helm Repo
```
helm repo list
helm repo add bitnami https://charts.bitnami.com/bitnami
```

## Create a values file
Default values here: https://github.com/bitnami/charts/blob/master/bitnami/mysql/values.yaml 

Create a local one to override some values:  
mysql/software-tracker-db.yaml

There will be a `root` user created with password.  
Another user `toladmin` created with password, which values will be set in the command line.  
And also a readonly user `tol`.

## How to trigger additional initial SQL in Kubernetes
The sqls added to the values as initdbScripts.

## Install the services
```
k create ns tol-software-tracking (if not created yet)
k config set-context --current --namespace=tol-software-tracking

# Add password value when you run
helm install software-tracker-db-tol bitnami/mysql -f mysql/software-tracker-db.yaml \
--set "auth.username=toladmin" \
--set "auth.password= " \
--dry-run

# Add password value when you run
helm install software-tracker-db-tol bitnami/mysql -f mysql/software-tracker-db.yaml \
--set "auth.username=toladmin" \
--set "auth.password= " \

# retrieve root password
MYSQL_ROOT_PASSWORD=$(kubectl get secret --namespace tol-software-tracking software-tracker-db-tol-mysql -o jsonpath="{.data.mysql-root-password}" | base64 --decode)

# retrieve non root password
MYSQL_ROOT_PASSWORD=$(kubectl get secret --namespace tol-software-tracking software-tracker-db-tol-mysql -o jsonpath="{.data.mysql-password}" | base64 --decode)

# upgrade
ROOT_PASSWORD=$(kubectl get secret --namespace tol-software-tracking software-tracker-db-tol-mysql -o jsonpath="{.data.mysql-root-password}" | base64 --decode)
helm upgrade --namespace tol-software-tracking software-tracker-db-tol bitnami/mysql --set auth.rootPassword=$ROOT_PASSWORD

helm uninstall software-tracker-db-tol
k delete pvc data-tracker-db-mysql-0
```

## Notes from Helm Installation
```text

CHART NAME: mysql
CHART VERSION: 8.9.6
APP VERSION: 8.0.29

** Please be patient while the chart is being deployed **

Tip:

  Watch the deployment status using the command: kubectl get pods -w --namespace tol-software-tracking

Services:

  echo Primary: software-tracker-db-tol-mysql.tol-software-tracking.svc.cluster.local:3306

Execute the following to get the administrator credentials:

  echo Username: root
  MYSQL_ROOT_PASSWORD=$(kubectl get secret --namespace tol-software-tracking software-tracker-db-tol-mysql -o jsonpath="{.data.mysql-root-password}" | base64 --decode)

To connect to your database:

  1. Run a pod that you can use as a client:

      kubectl run software-tracker-db-tol-mysql-client --rm --tty -i --restart='Never' --image  docker.io/bitnami/mysql:8.0.29-debian-10-r2 --namespace tol-software-tracking --env MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD --command -- bash

  2. To connect to primary service (read/write):

      mysql -h software-tracker-db-tol-mysql.tol-software-tracking.svc.cluster.local -uroot -p"$MYSQL_ROOT_PASSWORD"



To upgrade this helm chart:

  1. Obtain the password as described on the 'Administrator credentials' section and set the 'root.password' parameter as shown below:

      ROOT_PASSWORD=$(kubectl get secret --namespace tol-software-tracking software-tracker-db-tol-mysql -o jsonpath="{.data.mysql-root-password}" | base64 --decode)
      helm upgrade --namespace tol-software-tracking software-tracker-db-tol bitnami/mysql --set auth.rootPassword=$ROOT_PASSWORD
```

### Dev and Prod environments

We use the same setting for Dev and Prod environments, just switch the Kubernetes cluster and do Helm installation.


## Data migration

If the same version of database, we can copy the whole database file system. 

For different versions of database server, we can use `mysqldump` the whole database or one tables with column fileting, e.g.
```
# compress the dump file may improve the performance
mysqldump -u root -p --single-transaction --quick --skip-lock-tables software_tracker > dump.sql
mysqldump -u root -p --single-transaction --quick --skip-lock-tables software_tracker logging_event --where="timestamp >= '2025-01-01'" | gzip > dump_partial.sql.gz

# turn the following off, may improve the speed
SET autocommit=0;
SET unique_checks=0;
SET foreign_key_checks=0;

# It may take long time to restore the data, in this case, we can run it outside the pod. The login shell to the pod may be disconnected often.
zcat dump_partial.sql.gz | mysql -u root -p  -h 172.27.22.222 -P 31741 software_tracker

# turn back
SET autocommit=1;
SET unique_checks=1;
SET foreign_key_checks=1;

```
