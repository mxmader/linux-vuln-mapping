#!/usr/bin/env python2

import json
import os
import posixpath
import requests
import urlparse

distro = "centos"
distro_file = distro + "_repo_meta_sources.json"
download_base_dir = distro + "_repo_meta"
download_chunk_size = 131072

with open(distro_file, 'r') as file_handle:
	distro_data = json.loads(file_handle.read())
	
for version in distro_data:
	print "[" + distro + " " + version + "]"
	
	# skip the version if it doesn't have repo types & associated meta URLs defined
	if not distro_data[version]:
		continue
		
	for repo_type in distro_data[version]:
		print " Repo type: " + repo_type
		
		for meta_type, url_data in distro_data[version][repo_type].iteritems():

			download_url = url_data['url']
			download_dir = download_base_dir + "/" + version + "/" + repo_type
			download_file = download_dir + "/" + posixpath.basename(urlparse.urlsplit(download_url).path)
			print "  Download URL: " + download_url
			print "  Local file: " + download_file
			
			if not os.path.exists(download_dir):
				print "  Creating dir: " + download_dir
				os.makedirs(download_dir)
			
			print "  Downloading file (chunking via stream)"
			download_req = requests.get(download_url, stream=True)
			
			if download_req.status_code == 200:
				with open(download_file, 'wb') as file_handle:
					for chunk in download_req.iter_content(download_chunk_size):
						file_handle.write(chunk)


"""
# consider this for validating repo file downloads. will need to update repo version scraper to catalog checksum type and content from repomod.xml
import hashlib
hashlib.sha256('foo').hexdigest()
"""
