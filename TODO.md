# Ways to improve

- Find a way to remove most of the ".first()" references - those should really be ".one()".
  Perhaps need to track a list of known package oddities such as "comps.rpm"
- Deal with CVE outliers - those that didnt hit a match in the MITRE/NIST data sets. 
  Perhaps catalog known bugs in the upstream data and carry a filter to fix them on-the-fly (at ingestion/refresh time)
- Data refresh - lets not dump entire tables when there is new data
- "distro_version_package_file" could possibly be merged into "distro_version_package_provides" - probably need some deduping / "INSERT IGNORE" logic
- look into using the yum python libraries. may imply updating old EL 4.x and 5.x data structures to look like 6.x
- catalog dependency resolution "misses" and look into them 
 - For depsolving, consider the "package_version" table for explicit package deps - they don't always self-identify under the "package_version_provides" table
- add timing metrics - "took X sec to ingest major.minor" and perhaps for each step (checkpoint and cumulative)

# Ways to expand

- Add the NIST data
- Move the CVE relationship processing logic to use the NIST data instead (incl. related schema updates)
- Automated polling of new CVE / RPM data.
 - CVE may need periodic lookbehind to previous years since old (out of this year) CVEs do get updated on occasion
 - Catalog "currently supported" major/minor EL versions so we dont go grabbing data for versions under EOL constraints

- use real data models expressed in python as opposed to leaning on sqlsoup to "detect everything". 
  some tables have primary keys just to shut sqlsoup up / make it dumb and happy.
- If we really want CentOS 4.0 package groups, we'll need to extract those relationships in real 
  time when catalogging the "os/primary' data, or iterate back through that data afterwards

- RHEL / Scientific / Oracle Linux?
