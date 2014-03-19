#!/bin/bash

db_name=linux-meta
db_user=linuxmeta
db_pwd=AV3rry5tr0ngPa55W#rDMan
db_schema_file=linux-meta.sql

echo "Creating database instance: $db_name"
mysqladmin -uroot -p create $db_name

echo "Creating user: $db_user@localhost and adding grants for $db_name"
echo "GRANT ALL PRIVILEGES ON \`db_name\`.* to '$db_user'@'localhost' IDENTIFIED BY '$db_pwd';" | mysql -uroot -p

echo "Importing linux-meta schema"
cat $db_schema_file | mysql -u$db_user -p$db_pwd -D $db_name
