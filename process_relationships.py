#!/usr/bin/env python2

from repo_meta import repo_ingestion
import json
import os
import pprint
import sys
import sqlalchemy
import sqlsoup

distro = "centos"
distro_file = distro + "_repo_meta_sources.json"
download_base_dir = distro + "_repo_meta"
debug = True

# set debug level for utility classes
repo_ingestion.debug = debug

with open(distro_file, 'r') as file_handle:
	distro_data = json.loads(file_handle.read())

db = sqlsoup.SQLSoup('mysql://linux-meta:fershuretotallybro@localhost/linux-meta')
latest_versions = {}

# find the latest minor version of each major version & catalog them.
# we only care about those packages for group relationship purposes
for version in distro_data.iterkeys():
	
	# skip the version if it isn't well defined
	if version not in distro_data or not distro_data[version]:
		continue
	
	major_version, minor_version = version.split('.')
	
	if not major_version in latest_versions.iterkeys() or int(minor_version) > int(latest_versions[major_version]):
		latest_versions[major_version] = minor_version
	
# For each "latest major/minor version", create a list of generic package names in the DB.
# These are for relating to the package groups of the like version	
for major_version in sorted(latest_versions):
	
	version = major_version + '.' + latest_versions[major_version]
	print "processing",version
	
	print " + ingesting packages by name"
	
	# get the list of packages for this distro's latest version
	where = sqlalchemy.and_(
		db.distro.major_version == major_version,
		db.distro.minor_version == latest_versions[major_version]
	)
	
	# ingest the package group info & map distro-latest packages by name
	repo_type = 'os'
	meta_type = 'comps'
	repo_attributes = distro_data[version][repo_type][meta_type]
	repo_ingestor = repo_ingestion(distro_id, major_version)
	file_base_dir = download_base_dir + "/" + version + "/" + repo_type
	file_path = file_base_dir + "/" + repo_attributes['uncompressed_file_name']
	repo_ingestor.ingest_comps_xml(file_path)
	
	print " + mapping dependencies"
	
	# relate the top-level packages together
	for distro_package_version in distro_package_versions:
		
		where = sqlite.and_(
			package.distro_id == distro.id,
			distro_package_version_id == distro_package_version.id
		)

		package = db.package.filter(where).one()
		
		if self.debug:
			print package.id,package.name,package.release,"maps to",distro_package_version.id,distro_package_version.name,distro_package_version.version,distro_package_version.release
		
		# get the list of package's requirements
		requirements = db.distro_package_requires.filter(distro_package_version.id).all()
		
		# list of high-level package IDs required by this package
		requirements_list = []
		
		# go through each requirement and find a package to satisfy it
		for requirement in requirements:

			if requirement.type == 'library' or requirement.type == 'package':

				sql = "select distro_package_version.* from distro_package_version where id = " + distro.id + \
					  "and 
					  
					  "order by distro_package_version.version DESC"

				where = sqlite.and_(
					db.distro_package_version_provides.flags == requirement.flags,
					db.distro_package_version_provides.name == requirement.name,
					db.distro_package_version_provides.type == requirement.type,
					db.distro_package_version_provides.version == requirement.version
				)

				satisfied_by = db.distro_package_version_provides.filter(where).first()

				if not satisfied_by:
					if self.debug:
						print "  + could not satisfy requirement:",requirement.id
					continue

				if self.debug:
					print "  + requirement",requirement.id,"satisfied by:",satisfied_by.id
				
				# get the generic id for the dependency then map to the package (don't worry about dupes)
				where = sqlalchemy.and_(
					db.package.distro_id = distro.id,
					db.package.distro_package_version.id = satisfied_by.id
				)

				dependency_package = db.package.filter(where).one()

				# add this to the list of required packages if it's not already
				if not dependency_package.id:
					if self.debug:
						print "   + adding",dependency_package.id,"to list of deps"
					requirements_list.add(dependency_package.id)

			elif requirement.type == 'file':

				where = sqlalchemy.and_(
					db.distro_package_version_file.name == requirement.name
		
		# insert the deduped list of deps to the DB
		for dependency in requirements_list:

			db.package_to_required_package_map.insert(
				package_id = package.id,
				required_package_id = dependency
			)
			
		# commit this mapping
		db.commit()
			
				
	
	
		
		
