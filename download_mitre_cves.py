#!/usr/bin/env python2

from BeautifulSoup import BeautifulSoup as bsoup

import requests

# Get the list of MITRE CVE databases and download them
mitre_cve_catalog_url = "https://cve.mitre.org/data/downloads/"

tree = bsoup(mitre_cve_catalog_req.content)
mitre_downloads = tree.findAll('a', href=re.compile(r'^/data/downloads/.*\.xml'))

for mitre_download in mitre_downloads:
