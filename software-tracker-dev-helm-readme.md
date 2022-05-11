```
# make sure correct Kubernetes cluster being used, prod or dev?
k config get-contexts

# make sure mysql Helm chart being installed
helm list 

# make sure using the same namespace as mysql
k create namespace tol-software-tracking (if not created yet)
k config set-context --current --namespace=tol-software-tracking

# test helm template
# add the password for user toladmin when running the command
helm install software-tracker-app-tol software-tracker-app \
-f software-tracker-dev-values.yaml \
--set "database.rwPassword= " \
--dry-run

# helm install
# add the password for user toladmin when running the command
helm install software-tracker-app-tol software-tracker-app \
-f software-tracker-dev-values.yaml \
--set "database.rwPassword= "

NOTES:
1. Get the application URL by running these commands:
Ingress URL:
  http://paso.tol-dev.sanger.ac.uk/
NodePort Service:
  export NODE_PORT=$(kubectl get --namespace tol-software-tracking -o jsonpath="{.spec.ports[0].nodePort}" services software-tracker-app-tol)
  export NODE_IP=$(kubectl get nodes --namespace tol-software-tracking -o jsonpath="{.items[0].status.addresses[2].address}")
  echo http://$NODE_IP:$NODE_PORT

```