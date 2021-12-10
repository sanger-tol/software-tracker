```
export PASSWORD=
curl -k1 -u tolpipe:${PASSWORD} -H "Content-type: application/json" -X POST https://infoblox-gm.internal.sanger.ac.uk/wapi/v2.3.1/request -d @- < software-tracker-dns-dev.json

# on farm, checking
dnsgrep psao
```