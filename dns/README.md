# Create DNS entris for the paso sercices
```
# ask for password if you don't know
export PASSWORD=

# create DNS entry for dev server
curl -k1 -u tolpipe:${PASSWORD} -H "Content-type: application/json" -X POST https://infoblox-gm.internal.sanger.ac.uk/wapi/v2.3.1/request -d @- < software-tracker-dns-dev.json

# create DNS entry for prod server
curl -k1 -u tolpipe:${PASSWORD} -H "Content-type: application/json" -X POST https://infoblox-gm.internal.sanger.ac.uk/wapi/v2.3.1/request -d @- < software-tracker-dns-prod.json

# on farm, checking entries being created
dnsgrep paso
```