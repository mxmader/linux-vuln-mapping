#!/usr/bin/env python2

from bs4 import BeautifulSoup as bsoup

import glob
import os
import sqlsoup
import sys
import time

if "--debug" in sys.argv:
	debug = True
else:
	debug = False

if debug:
	print "getting list of MITRE CVE files (one per calendar year)"

files = glob.glob("mitre_cves/allitems-cvrf-year-*.xml")
files.sort()

for mitre_file in files:

	print "Processing", mitre_file

	with open(mitre_file) as mitre_file_handle:

		if debug:
			print "mapping XML into bsoup tree"

		tree = bsoup(mitre_file_handle.read(), ["lxml", "xml"])
		
	if debug:
		print "getting 'Vulnerability' elements"
	
	vulns = tree.find_all('Vulnerability')
	
	if debug:
		print "init db object"

	db = sqlsoup.SQLSoup('mysql://linux-meta:fershuretotallybro@localhost/linuxmeta')
	
	print " + Mapping CVE data"
	
	for index,vuln in enumerate(vulns):

		if debug:
			print "[" + str(index) + "]", vuln.CVE.text

		description = vuln.Notes.find('Note', attrs = { "Type" : "Description" }).text
		published = vuln.Notes.find('Note', attrs = { "Title" : "Published" })
		
		if published:
			published = published.text
						
		modified = vuln.Notes.find('Note', attrs = { "Title" : "Modified" })
			
		if modified:
			modified = modified.text
		elif published:
			modified = published

		db.mitre_cve.insert(				
				cve = vuln.CVE.text,
				description = description,
				published = published,
				modified = modified,
				title = vuln.Title.text
			)	

	print " + Committing CVE data"
	db.commit()

	if debug:
		print " + Waiting for commit to finish"

	time.sleep(5)

	print " + Mapping CVE Reference data"
	for index,vuln in enumerate(vulns):

		if vuln.References:
	
			for reference in vuln.References.find_all('Reference'):
					
				db.mitre_cve_reference.insert(
					cve = vuln.CVE.text,
					url = reference.URL.text,
					description = reference.Description.text
					)
		
	print " + Committing CVE Reference data"
	db.commit()

	del db
	del tree
