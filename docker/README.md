# PASO application and Docker image building

The following to build the image locally:
```
docker build -t software-tracker -f Dockerfile .
```

Normally the docker image will be built by GitHub action when you commit to the main branch and tag the repo.

And the docker image will be pushed to:  
https://github.com/sanger-tol/software-tracker/pkgs/container/software-tracker
