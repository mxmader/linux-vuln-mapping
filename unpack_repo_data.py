#!/usr/bin/env python2

import bz2
import gzip
import json
import os

distro = "centos"
distro_file = distro + "_repo_meta_sources.json"
download_base_dir = distro + "_repo_meta"
download_chunk_size = 131072
supported_compression_formats = [ 'gz', 'bzip2' ]

with open(distro_file, 'r') as file_handle:
	distro_data = json.loads(file_handle.read())
	
for version in distro_data:
	
	for repo_type in distro_data[version]:
		print "[", distro, version,"/",repo_type, "]"
		
		for meta_type, url_data in distro_data[version][repo_type].iteritems():
			
			download_url = url_data['url']
			repo_dir = download_base_dir + "/" + version + "/" + repo_type
			
			compressed_file_name = url_data['compressed_file_name']
			compressed_file_path = repo_dir + "/" + compressed_file_name
				
			uncompressed_file_name = url_data['uncompressed_file_name']
			uncompressed_file_path = repo_dir + "/" + uncompressed_file_name
	
			# Decompress the file, if applicable
			if url_data['compression_type'] in supported_compression_formats:
				
				# if the uncompressed file already exists, skip it
				if os.path.exists(uncompressed_file_path):
					print "  Uncompressed", url_data['compression_type'], "file exists:", uncompressed_file_name
					continue

				else:
					print "  " + url_data['compression_type'] + " decompressing: " + compressed_file_name
					
					if url_data['compression_type'] == 'gz':
				
						print "  Writing uncompressed file:", uncompressed_file_name
						
						with gzip.open(compressed_file_path, "rb") as compressed_file_handle, open(uncompressed_file_path, 'w') as uncompressed_file_handle:

							try:
							
								decoded = compressed_file_handle.read()	
								uncompressed_file_handle.write(decoded)
							
							except IOError, error:

								if str(error) == "Not a gzipped file":
									print "  Not actually compressed:",compressed_file_name, " - instead copying as", uncompressed_file_name
								
									with open(compressed_file_path, "r") as not_compressed_file_handle:
										uncompressed_file_handle.write(not_compressed_file_handle.read())								
								else:
									print "  Not sure what to do with:",compressed_file_name,"-",error_string

					elif url_data['compression_type'] == 'bz2':
						
						print "  Writing uncompressed file:", uncompressed_file_name
						
						with open(uncompressed_file_path, 'wb') as uncompressed_file_handle, bz2.BZ2File(compressed_file_path, 'rb') as compressed_file_handle:
							for data in iter(lambda : compressed_file_handle.read(100 * 1024), b''):
								uncompressed_file_handle.write(data)
				
					else:
						print "  Unknown compression type:", url_data['compression_type']
					
				
			else:
				print "  Uncompressed file exists without compressed parent:", uncompressed_file_name
				
				
			
			
