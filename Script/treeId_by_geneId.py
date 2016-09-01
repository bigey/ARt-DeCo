#!/usr/bin/env python

import requests, sys

geneId = sys.argv[1]

server = "http://rest.ensemblgenomes.org"
ext    = "/genetree/member/id/" + geneId + "?compara=fungi;sequence=none"

headers = \
{ \
    "Content-Type" : "application/json" \
}

r = requests.get(server+ext, headers=headers)

if not r.ok:
  r.raise_for_status()
  sys.exit()

decoded = r.json()
# print(repr(decoded))
# print(decoded['id'])

# print repr(decoded)
print decoded['id']
