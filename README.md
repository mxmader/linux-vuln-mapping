# Linux Metadata builder

The scripts in this repo are aimed at composing data elements suitable for populating an RDBMS with the following metadata of Enterprise Linux (RHEL, CentOS, Scientific Linux, and Oracle Linux) and its upstream sources (Fedora):

- Software package names, versions, and architectures
- Bugzillas solved across major/minor versions
- CVEs addressed across major/minor versions
- All known major and minor versions with parseable package repository metadata (primary, updates, other)


## Procedure

To build the data set from scratch, use this procedure from a system connected to the internet:

```console
cd /path/to/linux-metadata-builder

# build a JSON manifest of URLs to various CentOS repository metadata files for all supported versions
./get_centos_repo_urls.py

# download the repository metadata files from the URLs collected above
./download_repo_meta.py

# parse the repository metadata files and transform into a relational database
# TODO: complete this
./process_repo_meta.py


###################################
# optional / for future functionality
###################################

# download the MITRE CVE databases (xml)
./download_mitre_cves.py
```
