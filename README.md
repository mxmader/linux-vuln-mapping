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
cd /path/to/linux-metadata-builder

# build a JSON manifest of URLs to various CentOS repository metadata files for all supported versions
./get_centos_repo_urls.py

# download the repository metadata files from the URLs collected above
./download_repo_meta.py

# parse the repository metadata files and transform into a relational database
# iterate through package changelogs and extract CVE information
# TODO: complete this
#./process_repo_meta.py
```

## Optional / future functionality

```console
# download the MITRE CVE databases (xml)
./download_mitre_cves.py

# parse the MITRE CVE databases and transform into a relational database
# scan package CVE relationships in order to link the MITRE metadata to a CentOS package
# TODO: write this
#./process_mitre_cves.py

```


## References

[CentOS Vault](http://vault.centos.org/)
[MITRE CVE Data](https://cve.mitre.org/data/downloads/)
[MITRE CWE Info](http://cwe.mitre.org/data/index.html)\
[NIST Vulnerability Datasets](http://nvd.nist.gov/)
[NIST NVD/CVE Data](http://nvd.nist.gov/download.cfm#CVE_FEED)
