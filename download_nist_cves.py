#!/usr/bin/env python2

from BeautifulSoup import BeautifulSoup as bsoup

import os
import posixpath
import re
import requests
import urlparse

download_chunk_size = 131072
download_dir = "nist_cves"

if not os.path.exists(download_dir):
	print "Creating dir: " + download_dir
	os.makedirs(download_dir)

# Get the list of nist CVE databases and download them
nist_cve_catalog_url = "https://nvd.nist.gov/download.cfm"

nist_cve_catalog_req = requests.get(nist_cve_catalog_url)
tree = bsoup(nist_cve_catalog_req.content)
nist_downloads = tree.findAll('a', href=re.compile(r'http://static.nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-.*\.xml'))

for nist_download in nist_downloads:
	download_url = nist_download.get('href')
	download_url.replace("http", "https")
	download_file = download_dir + "/" + posixpath.basename(urlparse.urlsplit(download_url).path)
	print "Downloading " + download_url
	
	download_req = requests.get(download_url, stream=True)
	if download_req.status_code == 200:
		with open(download_file, 'wb') as file_handle:
			for chunk in download_req.iter_content(download_chunk_size):
				file_handle.write(chunk)
