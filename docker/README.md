The following to push the image to docker hub.
```
docker build -t guoyingqi/software-tracker -f docker/Dockerfile .
docker push guoyingqi/software-tracker
```

The following to push the image to internal sanger gitlab.
```
# create a token here
# https://gitlab.internal.sanger.ac.uk/tol-it/software-tracker/-/settings/access_tokens
export GITLAB_USER="gq2"
export GITLAB_TOKEN="pKgxMebMjL68Pr_rM-uL"

docker logout gitlab-registry.internal.sanger.ac.uk
echo $GITLAB_TOKEN | docker login -u $GITLAB_USER --password-stdin gitlab-registry.internal.sanger.ac.uk

docker build -t gitlab.internal.sanger.ac.uk/tol-it/farm5-etc/tracker:latest -f docker/Dockerfile .
docker push gitlab.internal.sanger.ac.uk/tol-it/farm5-etc/tracker:latest
```
