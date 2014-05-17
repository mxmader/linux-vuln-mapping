#!/usr/bin/env python2

import json
import os
import requests

distro = "centos"
distro_file = distro + "_repo_meta_sources.json"
download_base_dir = distro + "_repo_meta"
download_chunk_size = 131072

with open(distro_file, 'r') as file_handle:
	distro_data = json.loads(file_handle.read())
	
for version in sorted(distro_data.iterkeys()):
	print "[" + distro + " " + version + "]"
	
	# skip the version if it doesn't have repo types & associated meta URLs defined
	if not distro_data[version]:
		continue
		
	for repo_type in distro_data[version]:
		print " Repo type: " + repo_type
		
		for meta_type, repo_attributes in distro_data[version][repo_type].iteritems():

			download_url = repo_attributes['url']
			download_dir = download_base_dir + "/" + version + "/" + repo_type
			download_file = download_dir + "/"
			
			if repo_attributes['compression_type']:
				download_file += repo_attributes['compressed_file_name']
			else:
				download_file += repo_attributes['uncompressed_file_name']

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
# consider this for validating repo file downloads. will need to update repo version scraper to catalog checksum type and content from repomd.xml
import hashlib
hashlib.sha256('foo').hexdigest()
"""
