```
# make sure mysql Helm chart being installed
helm list 

# make sure using the same namespace as mysql
k create namespace pshpc (if not created yet)
k config set-context --current --namespace=pshpc

# test helm template
helm install software-tracker-app-tol software-tracker-app --dry-run > dump.yaml

helm install software-tracker-app-tol software-tracker-app

```