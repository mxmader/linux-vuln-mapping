#!/usr/bin/env python2

from BeautifulSoup import BeautifulSoup as bsoup
import json
import pprint
import requests
import re
import sys

# inputs
arch="x86_64"
repo_metadata_index_file="repomd.xml"

# outputs
repo_lineage = {}
output_file = "centos_repo_meta_sources.json"

# categories of repo metadata we care about
repo_meta_types = [ 'other', 'primary', 'filelists', 'comps' ]

# types of repos we care about
repo_types = [ "os", "updates"]

# minimum major version
min_major_version = 4

# root URL of vault data tree
vault_url = "http://vault.centos.org/"

# template base URL for a vaulted version
vaulted_release_url_template = vault_url + "major_version.minor_version/repo_type/" + arch + "/"

# regex for scraping versions from the vault index
version_regex = re.compile(r'[0-9]+\.[0-9]+\/')

## uncompiled regex for pulling out repodata sqlite and XML file URLs respectively (must sub-in data type then compile later)
# assume that sqlite is always bz2 compressed
sqlite_regex = r'repodata/.*data_type\.sqlite.bz2' 
# give 2 options for XML, compressed or uncompressed.
xml_gz_regex = r'repodata/.*data_type\.xml\.gz'
xml_regex = r'repodata/.*data_type\.xml'

# index of latest minor version discovered for given major version(s)
latest_minor_versions = {}

# Generic top-level URL for current major releases
current_release_url_template = "http://isoredirect.centos.org/centos/major_version/repo_type/" + arch + "/"

# The release note URL "template" should always point to the most recently released "current" distribution.
current_release_note_url_template = current_release_url_template + "RELEASE-NOTES-en-US.html"

# Loop through a set of current and future major versions and figure out if they are currently supported
# aka "not EOL" - this will tell us which major/minor versions are NOT "in the vault"
for major_version in range(5,10):
	
	# dealing with these as strings will make life easier elsewhere in the script
	major_version = str(major_version)
	
	# compose the release note URL for this major version
	release_note_url = re.sub("major_version", major_version, current_release_note_url_template)
	release_note_url = re.sub("repo_type", "os", release_note_url)

	# Gotta love inconsistent URLs across major versions...
	if major_version is "5":
		release_note_url = re.sub("en-US", "en_US", release_note_url)

	# Download the release note for the latest "non-vaulted" minor version of this major version
	release_note_req = requests.get(release_note_url)
	
	# The release note exists and is not empty. w00t! let's look into it some more
	if release_note_req.status_code == 200 and release_note_req.content:
		
		# Parse the "major.minor" version out of the release note
		version = re.search(r'CentOS-' + major_version + '\.[0-9]+', release_note_req.content).group().split('-')[1]
		
		# Keep this information for later use
		minor_version = str(version.split('.')[1])
		latest_minor_versions[major_version] = minor_version
		
		print "Found supported (non-EOL) major version: " + major_version + " with most recent minor version: " + minor_version
	
	# Maybe they abandoned the store and left town...
	else:
		print "Could not find a release note for major version: " + major_version + " - it's either vaulted, DNE yet, or the URL scheme has changed"

# get the list of all major/minor version CentOS repos from "the vault"
vault_repos_req = requests.get(vault_url)

# something's broken or changed WRT the vault
if vault_repos_req.status_code != 200:
	print "Could not get list of versions from vault. Response code: " + vault_repos_req.status_code + ", Response: " + vault_repos_req.content
	sys.exit(1)

# get the top-level links for each version's "os" and "updates" repos - skip "betas"
tree = bsoup(vault_repos_req.content)
matches = tree.findAll('a', href = version_regex)

# look at each link discovered - it should be a major/minor release version.
for link in matches:
	
	# parse out the version details
	version = link.get('href').replace('/', '')
	major_version, minor_version = version.split('.')
	
	repo_lineage[version] = {}
	
	# we only care about certain major versions and beyond for compatibility's sake
	if int(major_version) < min_major_version:
		print "[Skipping v" + version + " < " + str(min_major_version) + ".0]"
		continue;
	
	print ""
	print "[Processing v" + version + "]"
	
	# this particular version isn't actually in the vault - it's current
	if major_version in latest_minor_versions and latest_minor_versions[major_version] == minor_version:
		repo_url_template = current_release_url_template	

	# this version is in the vault
	else:
		repo_url_template = vaulted_release_url_template
	
	# set up the repo URL
	repo_url = repo_url_template.replace("major_version", major_version)
	repo_url = repo_url.replace("minor_version", minor_version)
	
	# examine each data type in this repo
	for repo_type in repo_types:
		
		repo_lineage[version][repo_type] = {}
		
		print " <" + repo_type + ">"
		
		repo_type_url = repo_url.replace("repo_type", repo_type)
		repodata_url = repo_type_url + "repodata/"
		repomd_url = repodata_url + repo_metadata_index_file
		repomd_xml_req = requests.get(repomd_url)
		
		if repomd_xml_req.status_code != 200:
			print " Could not get " + repo_type + " repo metadata XML for version: " + version + " using URL: " + repomd_url
			continue
			
		tree = bsoup(repomd_xml_req.content, selfClosingTags=['location'])
		
		# get the URL for each repo metadata type (primary, other, etc)
		for repo_meta_type in repo_meta_types:

			# Update repos don't have group info (as of this writing); skip them
			if repo_type == 'updates' and repo_meta_type == 'comps':
				continue;
			
			data_type = ""
			compression_type = ""
			
			# try to find a sqlite db - preferred
			sqlite_href_regex = re.compile(sqlite_regex.replace("data_type", repo_meta_type))
			data_match = tree.findAll('location', href = sqlite_href_regex)

			# Found a SQLite URL.
			if data_match:
				data_type = "sqlite"
				compression_type = "bz2"

			# didn't find sqlite. try xml_gz
			else:

				xml_gz_href_regex = re.compile(xml_gz_regex.replace("data_type", repo_meta_type))
				data_match = tree.findAll('location', href = xml_gz_href_regex)

				if data_match:
					compression_type = "gz"
					data_type = "xml"
				else:
					xml_href_regex = re.compile(xml_regex.replace("data_type", repo_meta_type))
					data_match = tree.findAll('location', href = xml_href_regex)

					if data_match:
						data_type = "xml"

			# couldn't find xml. give up
			if not data_type:
				print "  - No URL found for: " + repo_meta_type
				continue
					
			data_url = repo_type_url + data_match[0].get('href')
			repo_lineage[version][repo_type][repo_meta_type] = {}
			repo_lineage[version][repo_type][repo_meta_type]['compression_type'] = compression_type
			repo_lineage[version][repo_type][repo_meta_type]['data_type'] = data_type
			repo_lineage[version][repo_type][repo_meta_type]['url'] = data_url
			print "  + " + repo_meta_type + " data: " + data_url

print ""
print "Writing data to: " + output_file
with open(output_file, 'w') as file:
	file.write(json.dumps(repo_lineage))
