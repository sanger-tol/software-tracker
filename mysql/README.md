# BITNAMI MYSQL STACK HELM CHARTS

## Links
Helm: https://bitnami.com/stack/mysql/helm  
Helm Source: https://github.com/bitnami/charts/tree/master/bitnami/mysql/#installing-the-chart  

Docker: https://hub.docker.com/r/bitnami/mysql  
Docker Source: https://github.com/bitnami/bitnami-docker-mysql  

Do we want to depend on these resources?

## Add Helm Repo
```
helm repo list
helm repo add bitnami https://charts.bitnami.com/bitnami
```

## Create a values file
Default values here: https://github.com/bitnami/charts/blob/master/bitnami/mysql/values.yaml 

Create a local one to override some values:  
mysql/tracker-db-dev.yaml 

There will be a root user created with password, and another user tol2 created with password.

## How to trigger additional initial SQL in Kubernetes
Create extra user toladmin with some permissions and a readonly user called tol.
Create tables.
The sqls added to the values as initdbScripts.

## Install the services
```
k create namespace pshpc (if not created yet)
k config set-context --current --namespace=pshpc

helm install software-tracker-db-tol bitnami/mysql -f mysql/software-tracker-db.yaml.yaml

ROOT_PASSWORD=$(kubectl get secret --namespace pshpc tracker-db-mysql -o jsonpath="{.data.mysql-root-password}" | base64 --decode)
helm upgrade --namespace pshpc software-tracker-db-tol bitnami/mysql --set auth.rootPassword=$ROOT_PASSWORD

helm uninstall software-tracker-db-tol
k delete pvc data-tracker-db-mysql-0
```

## Notes from Helm Installation
```text
** Please be patient while the chart is being deployed **

Tip:

  Watch the deployment status using the command: kubectl get pods -w --namespace pshpc

Services:

  echo Primary: tracker-db-mysql.pshpc.svc.cluster.local:3306

Administrator credentials:

  echo Username: root
  echo Password : $(kubectl get secret --namespace pshpc tracker-db-mysql -o jsonpath="{.data.mysql-root-password}" | base64 --decode)

To connect to your database:

  1. Run a pod that you can use as a client:

      kubectl run tracker-db-mysql-client --rm --tty -i --restart='Never' --image  docker.io/bitnami/mysql:8.0.26-debian-10-r10 --namespace pshpc --command -- bash

  2. To connect to primary service (read/write):

      mysql -h tracker-db-mysql.pshpc.svc.cluster.local -uroot -p my_database



To upgrade this helm chart:

  1. Obtain the password as described on the 'Administrator credentials' section and set the 'root.password' parameter as shown below:

      ROOT_PASSWORD=$(kubectl get secret --namespace pshpc tracker-db-mysql -o jsonpath="{.data.mysql-root-password}" | base64 --decode)
      helm upgrade --namespace pshpc tracker-db bitnami/mysql --set auth.rootPassword=$ROOT_PASSWORD
```

## Connect MySQL server using NodePort
```
mysql -h $NODE_IP -P$NODE_PORT -utol -ptol my_database
```
