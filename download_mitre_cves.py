#!/usr/bin/env python2

from BeautifulSoup import BeautifulSoup as bsoup

import os
import posixpath
import re
import requests
import urlparse

download_chunk_size = 131072
download_dir = "mitre_cves"

if not os.path.exists(download_dir):
	print "Creating dir: " + download_dir
	os.makedirs(download_dir)

# Get the list of MITRE CVE databases and download them
mitre_base_url = "https://cve.mitre.org"
mitre_cve_catalog_url = mitre_base_url + "/data/downloads"

mitre_cve_catalog_req = requests.get(mitre_cve_catalog_url)
tree = bsoup(mitre_cve_catalog_req.content)
mitre_downloads = tree.findAll('a', href=re.compile(r'^/data/downloads/.*\.xml'))

for mitre_download in mitre_downloads:
	href = mitre_download.get('href')
	download_url = mitre_base_url + href
	download_file = download_dir + "/" + posixpath.basename(urlparse.urlsplit(download_url).path)
	print "Downloading " + download_url
	
	download_req = requests.get(download_url, stream=True)
	if download_req.status_code == 200:
		with open(download_file, 'wb') as file_handle:
			for chunk in download_req.iter_content(download_chunk_size):
				file_handle.write(chunk)
