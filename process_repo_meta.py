#!/usr/bin/env python2

from repo_meta import repo_ingestion
from repo_meta import distro_ingestion
import json
import os
import pprint
import sys

distro = "centos"
distro_file = distro + "_repo_meta_sources.json"
download_base_dir = distro + "_repo_meta"
debug = False

# set debug level for utility classes
repo_ingestion.debug = debug
distro_ingestion.debug = debug

# define the ingestion sequence
ingestion_sequence = [
	{ "os" : "primary" },
	{ "os" : "filelists" },
	{ "os" : "other" },
	{ "os" : "comps" },
	{ "updates" : "primary" },
	{ "updates" : "filelists" },
	{ "updates" : "other" }
]

with open(distro_file, 'r') as file_handle:
	distro_data = json.loads(file_handle.read())

if len(sys.argv) == 2:
	version_list = [ sys.argv[1] ]
else:
	version_list = sorted(distro_data.iterkeys())

for version in version_list:
	
	# skip the version if it isn't well defined
	if version not in distro_data or not distro_data[version]:
		print "Skipping:", version
		continue
		
	print "[" + distro + " " + version + "]"
	
	# figure out the major/minor versions, catalog this distro/version in the DB
	major_version, minor_version = version.split('.')
	distro_ingestor = distro_ingestion()
	distro_id = distro_ingestor.ingest_distro(major_version, minor_version)
	
	# initialize the repo meta ingestion instance. we'll re-use it for each repo (os, updates) & meta type (primary, other, filelists, comps).
	repo_ingestor = repo_ingestion(distro_id, major_version)
	
	for ingestion in ingestion_sequence:
		
		for repo_type,meta_type in ingestion.iteritems():
			
			# the desired meta type isn't available. this happens typically when "comps" are not there in old major versions.
			if not meta_type in distro_data[version][repo_type]:
				print " - no " + meta_type + " available"
				continue				
			
			repo_attributes = distro_data[version][repo_type][meta_type]
			print " +",repo_type + ":", meta_type + ":", repo_attributes['data_type']		

			file_base_dir = download_base_dir + "/" + version + "/" + repo_type
			file_path = file_base_dir + "/" + repo_attributes['uncompressed_file_name']
			
			repo_func_name = "ingest_" + meta_type + "_" + repo_attributes['data_type']
			repo_func = getattr(repo_ingestor, repo_func_name)
			repo_func(file_path)
		
	# At this point all meta types should be ingested. Now we can form
	# relationships (requires) between package versions
	repo_ingestor.map_dependencies()
