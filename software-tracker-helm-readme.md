```
# make sure mysql Helm chart being installed
helm list 

# make sure using the same namespace as mysql
k create namespace pshpc (if not created yet)
k config set-context --current --namespace=pshpc

# test helm template
helm install software-tracker-app-tol software-tracker-app --dry-run > dump.yaml

helm install software-tracker-app-tol software-tracker-app

NOTES:
1. Get the application URL by running these commands:
NodePort Service:
  export NODE_PORT=$(kubectl get --namespace pshpc -o jsonpath="{.spec.ports[0].nodePort}" services software-tracker-app-tol)
  export NODE_IP=$(kubectl get nodes --namespace pshpc -o jsonpath="{.items[0].status.addresses[2].address}")
  echo http://$NODE_IP:$NODE_PORT

```