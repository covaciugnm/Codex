#!/usr/bin/env python3
# Adauga IP-ul releului hosterion (185.199.175.100) in SPF-ul zonelor Cloudflare ac-wohnart.at, eva-org.com, cesiro.com.
import json, sys, urllib.request
tok = sys.argv[1]
H = {"Authorization": "Bearer " + tok, "Content-Type": "application/json"}
def api(method, path, data=None):
    req = urllib.request.Request("https://api.cloudflare.com/client/v4" + path,
                                 data=json.dumps(data).encode() if data else None, headers=H, method=method)
    return json.load(urllib.request.urlopen(req))
zones = {"ac-wohnart.at": "98ad0678272739bc90bd50b27e4ab7d2",
         "eva-org.com": "e8ea7c555f8a711d4efb4b556211987f",
         "cesiro.com": "14a5de4ed3c9c8fc391745e83caa343c"}
ADD = "ip4:185.199.175.100"
for z, zid in zones.items():
    recs = api("GET", "/zones/%s/dns_records?type=TXT&name=%s&per_page=50" % (zid, z))["result"]
    spf = [r for r in recs if r["content"].strip('"').startswith("v=spf1")]
    print("==", z, "SPF records:", len(spf))
    for r in spf:
        old = r["content"].strip('"')
        if ADD in old:
            print("  deja contine:", old); continue
        parts = old.split(); parts.insert(len(parts) - 1, ADD); new = " ".join(parts)
        res = api("PATCH", "/zones/%s/dns_records/%s" % (zid, r["id"]), {"content": new})
        print("  OLD:", old); print("  NEW:", res["result"]["content"], "| success:", res["success"], res.get("errors"))
