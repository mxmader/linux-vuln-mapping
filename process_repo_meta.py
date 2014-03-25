#!/usr/bin/env python2

import gzip
import json
import os
import posixpath
import urlparse

distro = "centos"
distro_file = distro + "_repo_meta_sources.json"
download_base_dir = distro + "_repo_meta"
download_chunk_size = 131072

with open(distro_file, 'r') as file_handle:
	distro_data = json.loads(file_handle.read())
	
for version in distro_data:
	print "[" + distro + " " + version + "]"
	
	for repo_type in distro_data[version]:
		print " Repo type: " + repo_type
		
		for meta_type, url_data in distro_data[version][repo_type].iteritems():
			
			download_url = url_data['url']
			
			# Decompress the file, if applicable
			if url_data['compression_type']:

				compressed_file_name = posixpath.basename(urlparse.urlsplit(download_url).path)
				compressed_file_path = download_base_dir + "/" + compressed_file_name
				
				uncompressed_file_name = compressed_file_name.replace('.' + url_data['compression_type'], '')
				uncompressed_file_path = download_base_dir + "/" + uncompressed_file_name
				
				if os.path.exists(uncompressed_file_path):
					print " Uncompressed " + url_data['compression_type'] + " file exists: " + uncompressed_file_name
				else:
					print " " + url_data['compression_type'] + " decompressing: " + compressed_file_name
					
					if url_data['compression_type'] == 'gz':
						
						with gzip.open(compressed_file_path, "rb") as gzip_file_handle:
							with open(uncompressed_file_path, 'w') as flat_file_handle:

								decoded = gzip_file_handle.read()
								flat_file_handle.write(decoded)

					elif url_data['compression_type'] == 'bz2':
						
						print "bz2 not yet implemented"
				
					
				
			else:
				uncompressed_file_name = posixpath.basename(urlparse.urlsplit(download_url).path)
				uncompressed_file_path = download_base_dir + "/" + file_name
				
				
			
			
