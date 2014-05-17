# Linux Metadata builder

The scripts in this repo are aimed at composing data elements suitable for populating an RDBMS with the following metadata 
of Enterprise Linux (RHEL, CentOS, Scientific Linux, and Oracle Linux) and its upstream sources (Fedora):

- Software package names, versions, and architectures
- Bugzillas solved across major/minor versions
- CVEs addressed across major/minor versions
- All known major and minor versions with parseable package repository metadata (primary, updates, other)

## Support posture

At this time, CentOS major versions 4 through 6 are supported.
If the metadata structure as well as repository directory layout of future CentOS 
releases matches any of these major versions, they should also be discovered / imported.

## Procedure

To build the data set from scratch, use this procedure from a system connected to the internet:

```console
# install the necessary python modules (list compiled from a Fedora 20 host referencing PyPI)
yum install -y mariadb-devel (needed to build MySQL-python)
pip install --upgrade beautifulsoup4 beautifulsoup lxml MySQL-python requests sqlsoup

cd /path/to/linux-metadata-builder

# build a JSON manifest of URLs to various CentOS repository metadata files for all supported versions
./get_repo_meta_sources.py

# download the repository metadata files from the URLs collected above
./download_repo_meta.py

# decompress the repo metadata files
./unpack_repo_meta.py

# give the DB schema setup script the mariaDB root password (you'll be prompted multiple times otherwise)
export db_root_pw=your_maria_root_password

# configure the MariaDB (or MySQL) schema
./setup_db.sh

# parse the repository metadata files and transform into a relational database
# iterate through package changelogs and extract CVE information
./process_repo_meta.py

```

## Optional - import MITRE CVE data

```console
# download the MITRE CVE databases (xml)
./download_mitre_cves.py

# parse the MITRE CVE database and transform into a relational database
# TODO: write this
#./process_mitre_cves.py

```


## References

[CentOS Vault](http://vault.centos.org/)
[MITRE CVE Data](https://cve.mitre.org/data/downloads/)
[MITRE CWE Info](http://cwe.mitre.org/data/index.html)\
[NIST Vulnerability Datasets](http://nvd.nist.gov/)
[NIST NVD/CVE Data](http://nvd.nist.gov/download.cfm#CVE_FEED)
