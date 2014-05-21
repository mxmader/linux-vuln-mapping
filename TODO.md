# Ways to improve

- Find a way to remove most of the ".first()" references - those should really be ".one()". Perhaps need to track a list of known package oddities such as "comps.rpm"
- Deal with CVE outliers - those that didnt hit a match in the MITRE/NIST data sets. Perhaps catalog known bugs in the upstream data and carry a filter to fix them on-the-fly (at ingestion/refresh time)
- Data refresh - lets not dump entire tables when there is new data


# Ways to expand

- Add the NIST data
- Move the CVE relationship processing logic to use the NIST data instead (incl. related schema updates)
- Automated polling of new CVE / RPM data.
 - CVE may need periodic lookbehind to previous years since old (out of this year) CVEs do get updated on occasion
 - Catalog "currently supported" major/minor EL versions so we dont go grabbing data for versions under EOL constraints
