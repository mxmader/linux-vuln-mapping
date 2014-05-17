from bs4 import BeautifulSoup as bsoup
import posixpath
import re
import sqlsoup
import sqlalchemy

class distro_ingestion:
	
	db = sqlsoup.SQLSoup('mysql://linux-meta:fershuretotallybro@localhost/linux-meta')
	debug = False
	
	def __init__(self):
		pass
	
	# Generic distro ingestion functions
	def ingest_distro(self, major_version, minor_version):
	
		distro = self.db.distro.insert(
			name = "CentOS",
			family = "enterprise",
			major_version = int(major_version),
			minor_version = int(minor_version)
		)
		
		try:
			self.db.commit()
		
		# ignore dupes
		except sqlalchemy.exc.IntegrityError:
			pass
			
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

	# different major versions have their own xml tags in certain cases. here, we catalog them.
	rpm_requires_tag = { 4 : 'requires', 5 : 'requires' }
	rpm_provides_tag = { 4 : 'provides', 5 : 'provides' }
	rpm_entry_tag    = { 4 : 'entry',    5 : 'entry'    }

	def __init__(self, distro_id, major_version):
		if self.debug:
			print "Initializing"		
			
		self.distro_id = distro_id
		self.major_version = major_version
		self.lib_matcher = re.compile(self.lib_match_regex)
		self.rpmlib_matcher = re.compile(self.rpmlib_match_regex)
		self.file_path_matcher = re.compile(self.file_path_match_regex)

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
	def fill_missing_package_dep_data(self, dependency):

		for key in ['flags', 'ver', 'epoch', 'pre', 'rel']:
			if key not in dependency:
				dependency[key] = ""
		
		return dependency
	
	##############################
	# SQLite ingestion functions
	##############################
	def ingest_primary_sqlite(self, file_path):
		print " " ,file_path

	def ingest_other_sqlite(self, file_path):
		print " " ,file_path

	# We don't care about filelists at the moment
	def ingest_filelists_sqlite(self, file_path):
		pass
	##############################
	# XML ingestion functions
	##############################
	
	
	def ingest_comps_xml(self, file_path, distro_id):
		
		tree = bsoup(self.get_file_content(file_path), ['lxml', 'xml'])
		groups = tree.find_all('group')
		
		for group in groups:

			if self.debug:
				print " ",group.id.text

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
		
			packages = group.packagelist.find_all('packagereq')

			for package in packages:
			
				if self.debug:	
					print "  ",package.text
				
				# TODO: Find the ID for this package 
				
				"""
				 self.db.package_to_distro_group_map.insert(
					package_id = my_package_id
					package_group_id = my_package_group.id
				 )
				 """

	def ingest_filelists_xml(self, file_path):
		pass

	def ingest_other_xml(self, file_path):
		print " " ,file_path

	def ingest_primary_xml(self, file_path):
		
		tree = bsoup(self.get_file_content(file_path), ['lxml', 'xml'])
		packages = tree.find_all('package')
		rpm_requires_tag = self.rpm_requires_tag[self.major_version]
		rpm_provides_tag = self.rpm_provides_tag[self.major_version]
		rpm_entry_tag = self.rpm_entry_tag[self.major_version]
		
		for package in packages:
			
			name = package.find('name').text
			
			if self.debug:
				print " ",name,package.version['ver']
			
			distro_package_version = self.db.distro_package_version.insert(
				distro_id = self.distro_id,
				name = name,
				arch = package.arch.text,
				version = package.version['ver'],
				release = package.version['rel'],
				epoch = package.version['epoch'],
				full_name = posixpath.basename(package.location['href'])
				)
			
			self.db.commit()

			provided_things = package.find(rpm_provides_tag).find_all(rpm_entry_tag)
			
			for function in provided_things:

				function = self.fill_missing_package_dep_data(function)

				self.db.distro_package_version_function.insert(
					distro_package_version_id = distro_package_version.id,
					flags = function['flags'],
					name = function['name'],
					type = self.get_rpm_relation_type(function['name']),
					version = function['ver']
				)
					
			dependencies = package.find(rpm_requires_tag).find_all(rpm_entry_tag)

			for dependency in dependencies:

				dependency = self.fill_missing_package_dep_data(dependency)

				self.db.distro_package_version_dependency.insert(
					distro_package_version_id = distro_package_version.id,
					flags = dependency['flags'],
					name = dependency['name'],
					type = self.get_rpm_relation_type(dependency['name']),
					version = dependency['ver']
				)
			
			if self.debug:
				print "   Committing deps and provided functionality"
				
			self.db.commit()		
