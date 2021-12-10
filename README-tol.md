# Set up software tracker database and web server in Kubernetes

1. Helm install mysql, see [mysql](mysql/README.md)
2. Create docker image for web application, see [docker](docker/README.md)
3. Create dns, see [dns](dns/README.md), [paso.tol-dev.sanger.ac.uk](http://paso.tol-dev.sanger.ac.uk/)
4. Check Helm [values](software-tracker-app/values.yaml) with correct details, especially database details, you may create a new values file.
5. Helm install web application, see [helm web install](software-tracker-helm-readme.md)
