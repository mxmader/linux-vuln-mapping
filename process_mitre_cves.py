#!/usr/bin/env python2

from bs4 import BeautifulSoup as bsoup

import glob
import os
import sqlsoup

print "getting list of MITRE CVE files (one per calendar year)"
files = glob.glob("mitre_cves/allitems-cvrf-year-*.xml")
files.sort()

print "init db object"
db = sqlsoup.SQLSoup('mysql://linux-meta:fershuretotallybro@localhost/linux-meta')

for mitre_file in files:

	print "processing", mitre_file

	with open(mitre_file) as mitre_file_handle:

		print "mapping XML into bsoup tree"
		tree = bsoup(mitre_file_handle.read(), ["lxml", "xml"])
		
		vulns = tree.find_all('Vulnerability')
		db_cve = db
		db_cve_reference = db
		
		for index,vuln in enumerate(vulns):

			print "[" + str(index) + "]", "processing",vuln.CVE.text
			description = vuln.Notes.find('Note', attrs = { "Type" : "Description" }).text
			
			if "** RESERVED **" in description:
				print "  Skipping - reserved"
				continue

			published = vuln.Notes.find('Note', attrs = { "Title" : "Published" })
			
			if published:
				published = published.text
						
			modified = vuln.Notes.find('Note', attrs = { "Title" : "Modified" })
			
			if modified:
				modified = modified.text
			elif published:
				modified = published

			db_cve.cve.insert(				
					cve = vuln.CVE.text,
					description = description,
					published = published,
					modified = modified,
					title = vuln.Title.text
				)	

			if vuln.References:
	
				for reference in vuln.References.find_all('Reference'):
					
					db_cve_reference.cve_reference.insert(
						cve = vuln.CVE.text,
						url = reference.URL.text,
						description = reference.Description.text
						)
	
		db_cve.commit()
		db_cve_reference.commit()

		db_cve.delete
		db_cve_reference.delete

		tree.delete
