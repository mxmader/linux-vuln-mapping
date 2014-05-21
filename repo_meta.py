from bs4 import BeautifulSoup as bsoup
from sqlalchemy.orm.exc import NoResultFound as NoResultFound
import posixpath
import pprint
import re
import sqlsoup
import sqlalchemy

class distro_ingestion:
	
	# hardcoded values that need to change in future for other distro support
	distro_name = "CentOS"
	distro_family = "enterprise"
		
	db = sqlsoup.SQLSoup('mysql://linux-meta:fershuretotallybro@localhost/linux-meta')
	debug = False
	
	def __init__(self):
		pass
	
	# Generic distro ingestion functions
	def ingest_distro(self, major_version, minor_version):
	
		major_version = int(major_version)
		minor_version = int(minor_version)

		where = sqlalchemy.and_(
			self.db.distro.name == self.distro_name,
			self.db.distro.family == self.distro_family,
			self.db.distro.major_version == major_version,
			self.db.distro.minor_version == minor_version
		)

		try:
			distro = self.db.distro.filter(where).one()
			if self.debug:
				print "  distro already exists"
		
		except NoResultFound:
	
			if self.debug:
				print "  adding distro"
				
			distro = self.db.distro.insert(
				name = self.distro_name,
				family = self.distro_family,
				major_version = major_version,
				minor_version = minor_version
			)
		
			self.db.commit()

		return distro.id
	

class repo_ingestion:
	
	db = sqlsoup.SQLSoup('mysql://linux-meta:fershuretotallybro@localhost/linux-meta')
	debug = False
	
	distro_id = None
	major_version = None
	
	# used to detect file-based package dependencies
	file_path_match_regex = r'^/\w+'
	file_path_matcher = None
	
	# used to detect library-based package dependencies
	lib_match_regex = r'^lib.*\(.*\)'
	lib_matcher = None
	
	# used to detect rpmlib package dependencies (and usually ignore them)
	rpmlib_match_regex = r'^rpmlib\(.*\)'
	rpmlib_matcher = None

	# used to detect changelogs with CAN/CVE references
	can_match_regex = r'(CAN\-[0-9]+\-[0-9]+)'
	can_matcher = None
	
	cve_match_regex = r'(CVE\-[0-9]+\-[0-9]+)'
	cve_matcher = None

	# catalog some commonly used xml tags
	rpm_requires_tag = 'requires'
	rpm_provides_tag = 'provides'
	rpm_entry_tag    = 'entry'
	package_tag = 'package'

	def __init__(self, distro_id, major_version):
		if self.debug:
			print "Initializing repo ingestion"		
			
		self.distro_id = distro_id
		self.major_version = int(major_version)
		self.lib_matcher = re.compile(self.lib_match_regex)
		self.rpmlib_matcher = re.compile(self.rpmlib_match_regex)
		self.file_path_matcher = re.compile(self.file_path_match_regex)
		self.can_matcher = re.compile(self.can_match_regex)
		self.cve_matcher = re.compile(self.cve_match_regex)

	def get_file_content(self, file_path):

		with open(file_path, 'r') as file_handle:
			return file_handle.read()

	# get the type of dependency or provided thing
	def get_rpm_relation_type(self, name):
		
		if self.lib_matcher.match(name):
			return 'library'
		elif self.file_path_matcher.match(name):
			return 'file'
		elif self.rpmlib_matcher.match(name):
			return 'rpmlib'	
		else:
			return 'package'
	
	# empty string-fill any missing package dep/provides data
	# TODO: consider the "defaultdict" module instead
	def fill_missing_package_dep_data(self, dependency):

		for key in ['flags', 'ver', 'epoch', 'pre', 'rel']:
			if key not in dependency:
				dependency[key] = ""
		
		return dependency
	
	##############################
	# SQLite ingestion functions
	##############################
	def ingest_primary_sqlite(self, file_path):
		
		sqlite_db = sqlsoup.SQLSoup("sqlite:///" + file_path)
		
		for package in sqlite_db.packages.all():

			if self.debug:
				print " ",package.name,package.version
			
			distro_package_version = self.db.distro_package_version.insert(
				distro_id = self.distro_id,
				arch = package.arch,
				checksum = package.pkgId,
				name = package.name,
				epoch = package.epoch,
				full_name = posixpath.basename(package.location_href),
				release = package.release,
				version = package.version			
				)
			
			# commit the package insert now so we get an id / primary key for it
			# to link child records
			self.db.commit()
	 
			provides = sqlite_db.execute("select * from provides where pkgKey = " + str(package.pkgKey))
				
			for name, flags, epoch, version, release, pkgKey in provides:

				# notice that the "name" property is cleansed of any non-ascii chars.
				# as of this writing i don't feel like preserving chinese characters (utf-X)
				# in font package feature names....
				self.db.distro_package_version_provides.insert(
					distro_package_version_id = distro_package_version.id,
					flags = flags,
					name = name.encode('ascii', 'ignore'),
					type = self.get_rpm_relation_type(name),
					version = version
				)
			
			requires = sqlite_db.execute("select * from requires where pkgKey = " + str(package.pkgKey))

			for name, flags, epoch, version, release, pkgKey, pre in requires:

				# see previous note about 'name' property sanitization
				self.db.distro_package_version_requires.insert(
					distro_package_version_id = distro_package_version.id,
					flags = flags,
					name = name.encode('ascii', 'ignore'),
					type = self.get_rpm_relation_type(name),
					version = version
				)
			
			if self.debug:
				print "   Committing deps and provided functionality"
				
			self.db.commit()		
			

	def ingest_other_sqlite(self, file_path):
		
		print " + processing SQLite other data"		
		sqlite_db = sqlsoup.SQLSoup("sqlite:///" + file_path)
		
		for package in sqlite_db.packages.all():
			
			# find the package from DB
			where = sqlalchemy.and_(
				self.db.distro_package_version.checksum == package.pkgId,
				self.db.distro_package_version.distro_id == self.distro_id
			)

			# fetch the package record
			distro_package_version = self.db.distro_package_version.filter(where).first()

			if self.debug:
				print "  +", distro_package_version.name, "looking for changelogs"	
				
			for pkgKey, author, date, changelog in sqlite_db.execute("select * from changelog where pkgKey = " + str(package.pkgKey)):
				
				# some older repo meta refers to CANs or "CVE Candidates". Treat
				# these as CVEs since they're catalogged as such by NIST/MITRE
				can_list = self.can_matcher.findall(changelog)
				
				#clean up the CAN list
				can_list = [can.replace('CAN', 'CVE') for can in can_list]
				cve_list = self.cve_matcher.findall(changelog)
				
				# concatenate the lists together (trusting that there's no dupes)
				cve_list = can_list + cve_list

				if cve_list:
					
					if self.debug:
						pprint.pprint(cve_list)

					for cve in cve_list:
						
						# add leading zeroes to non-4-digit CVE suffixes
						# e.g. CVE-2005-468 becomes "CVE-2005-0468"
						if len(cve) < 13:
							cve_parts = cve.split('-')
							cve_parts[2] = cve_parts[2].zfill(4)
							cve = '-'.join(cve_parts)

						# make sure this relationship doesn't exist (dont bother checking the "no match" table)
						where = sqlalchemy.and_(
							self.db.distro_package_version_cve.distro_package_version_id == distro_package_version.id,
							self.db.distro_package_version_cve.cve == cve
						)

						cve_map_check = self.db.distro_package_version_cve.filter(where).first()
						
						# relationship is already mapped; move on to the next package/CVE pair
						if cve_map_check:
							continue

						# if we can't find the linked CVE, then drop this into the "no match" table for later reference.
						try:
							self.db.mitre_cve.filter(self.db.mitre_cve.cve == cve).one()							

							if self.debug:
								print "    + mapping to package & mitre list:",cve

							self.db.distro_package_version_cve.insert(
								distro_package_version_id = distro_package_version.id,
								cve = cve
							)

						except NoResultFound:
							
							if self.debug:
								print "    + mapping to package & no_match:",cve
						
							self.db.distro_package_version_cve_no_match.insert(
								distro_package_version_id = distro_package_version.id,
								cve = cve
							)	
							continue
			
			# add this package's CVEs to the database
			self.db.commit()
		

	# We don't care about filelists at the moment
	def ingest_filelists_sqlite(self, file_path):
		
		print " + processing SQLite filelist data"
		sqlite_db = sqlsoup.SQLSoup("sqlite:///" + file_path)

		# compose a filelist insert transaction for each package
		for package in sqlite_db.packages.all():

			# find the package from DB
			where = sqlalchemy.and_(
				self.db.distro_package_version.checksum == package.pkgId,
				self.db.distro_package_version.distro_id == self.distro_id
			)

			# fetch the package record
			distro_package_version = self.db.distro_package_version.filter(where).first()

			if self.debug:
				print "  +", distro_package_version.name, "looking for files/dirs"			
			
			# collect the file names
			for pkgKey, dirname, filenames, filetypes in sqlite_db.execute("select * from filelist where pkgKey = " + str(package.pkgKey)):
				
				if self.debug:
					print "   + base dir",dirname
					print "   + file names",filenames
					print "   + file types",filetypes
				
				# pull apart file/dir list out of column
				file_items = filenames.split('/')
				
				# for every known file type, process its associated item (file or dir)
				for key, file_type in enumerate(list(filetypes)):
					
					item = file_items[key]
					
					if file_type == "f":
						file_type = "file"
					elif file_type == "d":
						file_type = "dir"
					
					# special case for files/dirs with fs root as the basedir
					if dirname == "/":
						file_path = dirname + item
					else:
						file_path = dirname + "/" + item
								
					if self.debug:
						print "   + adding", file_type + ":", file_path
					
					self.db.distro_package_version_file.insert(
						distro_package_version_id = distro_package_version.id,
						name = file_path,
						type = file_type
					)

			self.db.commit
		
	##############################
	# XML ingestion functions
	##############################
	
	def ingest_comps_xml(self, file_path):
		
		print " + processing XML comps data"
		tree = bsoup(self.get_file_content(file_path), ['lxml', 'xml'])
		
		for group in tree.find_all('group'):

			if self.debug:
				print "  +",group.id.text

			if group.description:
				description = group.description.text
			else:
				description = ""
			
			my_package_group = self.db.distro_package_group.insert(
				name = group.id.text,
				description = description,
				distro_id = distro_id
			)
			
			self.db.commit()

			for package in group.packagelist.find_all('packagereq'):
			
				if self.debug:	
					print "   +",package.text
				
				# Find the ID for this high-level (versionless) package
				my_package = self.db.package.filter(self.db.package.name == package.text).first()
				
				self.db.package_to_distro_group_map.insert(
					package_id = my_package.id,
					distro_package_group_id = my_package_group.id
				 )
				 
			if self.debug:
				print " + committing group to package map"
				
			self.db.commit()

	def ingest_filelists_xml(self, file_path):

		print " + processing XML filelist data"
		tree = bsoup(self.get_file_content(file_path), ['lxml', 'xml'])

		# compose a filelist insert transaction for each package
		for package in tree.find_all(self.package_tag):

			version_data = package.find('version')

			if self.debug:
				print "  +", package['name'], "looking for files/dirs"
				print package['arch'], version_data['epoch'],package['name'],version_data['rel'],version_data['ver'],self.distro_id
			
			
			# find the package from DB
			where = sqlalchemy.and_(
				self.db.distro_package_version.arch == package['arch'],
				self.db.distro_package_version.epoch == version_data['epoch'],
				self.db.distro_package_version.name == package['name'],
				self.db.distro_package_version.release == version_data['rel'],
				self.db.distro_package_version.version == version_data['ver'],
				self.db.distro_package_version.distro_id == self.distro_id
			)

			# fetch the package record
			distro_package_version = self.db.distro_package_version.filter(where).first()
			
			# collect the file names
			for file in package.find_all('file'):
				
				name = file.text.encode('ascii', 'ignore')
				
				if 'type' in file.attrs:
					file_type = file['type']
				else:
					file_type = 'file'
				
				if self.debug:
					print "   + adding", file_type + ":", name
					
				self.db.distro_package_version_file.insert(
					distro_package_version_id = distro_package_version.id,
					name = name,
					type = file_type
				)

			self.db.commit

	def ingest_other_xml(self, file_path):
		
		print " + processing XML other data"
		
		tree = bsoup(self.get_file_content(file_path), ['lxml', 'xml'])
		
		for package in tree.find_all('package'):
			
			if self.debug:
				print "  + looking up db for", package['name'], "by checksum:", package['pkgid']
			
			version_data = package.find('version')
			
			where = sqlalchemy.and_(
				self.db.distro_package_version.distro_id == self.distro_id,
				self.db.distro_package_version.arch == package['arch'],
				self.db.distro_package_version.epoch == version_data['epoch'],
				self.db.distro_package_version.checksum == package['pkgid'],
				self.db.distro_package_version.name == package['name'], 
				self.db.distro_package_version.release == version_data['rel'],
				self.db.distro_package_version.version == version_data['ver']
			)

			distro_package_version = self.db.distro_package_version.filter(where).first()
			
			for changelog in package.find_all('changelog'):
				
				# some older repo meta refers to CANs or "CVE Candidates". Treat
				# these as CVEs since they're catalogged as such by NIST/MITRE
				can_list = self.can_matcher.findall(changelog.text)
				
				#clean up the CAN list
				can_list = [can.replace('CAN', 'CVE') for can in can_list]
				cve_list = self.cve_matcher.findall(changelog.text)
				
				# concatenate the lists together (trusting that there's no dupes)
				cve_list = can_list + cve_list

				if cve_list:
					
					if self.debug:
						pprint.pprint(cve_list)

					for cve in cve_list:
						
						# add leading zeroes to non-4-digit CVE suffixes
						# e.g. CVE-2005-468 becomes "CVE-2005-0468"
						if len(cve) < 13:
							cve_parts = cve.split('-')
							cve_parts[2] = cve_parts[2].zfill(4)
							cve = '-'.join(cve_parts)

						# make sure this relationship doesn't exist (dont bother checking the "no match" table)
						where = sqlalchemy.and_(
							self.db.distro_package_version_cve.distro_package_version_id == distro_package_version.id,
							self.db.distro_package_version_cve.cve == cve
						)

						cve_map_check = self.db.distro_package_version_cve.filter(where).first()
						
						# relationship is already mapped; move on to the next package/CVE pair
						if cve_map_check:
							continue

						# if we can't find the linked CVE, then drop this into the "no match" table for later reference.
						try:
							self.db.mitre_cve.filter(self.db.mitre_cve.cve == cve).one()							

							if self.debug:
								print "    + mapping to package & mitre list:",cve

							self.db.distro_package_version_cve.insert(
								distro_package_version_id = distro_package_version.id,
								cve = cve
							)

						except NoResultFound:
							
							if self.debug:
								print "    + mapping to package & no_match:",cve
						
							self.db.distro_package_version_cve_no_match.insert(
								distro_package_version_id = distro_package_version.id,
								cve = cve
							)	
							continue
			
			# add this package's CVEs to the database
			self.db.commit()
		
		
	def ingest_primary_xml(self, file_path):
		
		print " + processing XML primary data"
		
		tree = bsoup(self.get_file_content(file_path), ['lxml', 'xml'])
		packages = tree.find_all(self.package_tag)
		
		for package in packages:
			
			name = package.find('name').text
			
			if self.debug:
				print " ",name,package.version['ver']
			
			distro_package_version = self.db.distro_package_version.insert(
				distro_id = self.distro_id,
				arch = package.arch.text,
				checksum = package.find('checksum', attrs={ 'pkgid' : 'YES'}).text,
				name = name,
				epoch = package.version['epoch'],
				full_name = posixpath.basename(package.location['href']),
				release = package.version['rel'],
				version = package.version['ver']			
				)
			
			self.db.commit()

			provides = package.find(self.rpm_provides_tag).find_all(self.rpm_entry_tag)
			
			for function in provides:

				function = self.fill_missing_package_dep_data(function)

				self.db.distro_package_version_provides.insert(
					distro_package_version_id = distro_package_version.id,
					flags = function['flags'],
					name = function['name'],
					type = self.get_rpm_relation_type(function['name']),
					version = function['ver']
				)
					
			requires = package.find(self.rpm_requires_tag).find_all(self.rpm_entry_tag)

			for dependency in requires:

				dependency = self.fill_missing_package_dep_data(dependency)

				self.db.distro_package_version_requires.insert(
					distro_package_version_id = distro_package_version.id,
					flags = dependency['flags'],
					name = dependency['name'],
					type = self.get_rpm_relation_type(dependency['name']),
					version = dependency['ver']
				)
			
			if self.debug:
				print "   Committing requirements and provided functionality"
				
			self.db.commit()		
