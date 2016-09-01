#!/usr/bin/env python3

import requests, sys
import sys
import os.path

if len(sys.argv) == 1:
    sys.exit(1)

treeId = sys.argv[1]

server = "http://rest.ensemblgenomes.org"
ext = "/genetree/id/" + treeId +"?nh_format=simple"

r = requests.get(server+ext, headers={ "Content-Type" : "text/x-nh"})

if not r.ok:
  r.raise_for_status()
  sys.exit()

print(r.text)
