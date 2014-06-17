#!/bin/bash

db_name=linuxmeta
db_user=linux-meta
db_pwd=fershuretotallybro
db_schema_file=linuxmeta.sql

echo "Dropping / Creating database instance: $db_name"
mysqladmin -uroot -p$db_root_pw --force drop $db_name
mysqladmin -uroot -p$db_root_pw create $db_name

echo "Creating user: $db_user@localhost and adding grants for $db_name"
echo "GRANT ALL PRIVILEGES ON \`$db_name\`.* to '$db_user'@'localhost' IDENTIFIED BY '$db_pwd';" | mysql -uroot -p$db_root_pw

echo "Importing linux-meta schema"
cat $db_schema_file | mysql -u"$db_user" -p"$db_pwd" -D $db_name
