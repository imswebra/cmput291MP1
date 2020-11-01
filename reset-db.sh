#!/bin/sh
rm -f database.db
sqlite3 database.db < sql/tables.sql
sqlite3 database.db < sql/data.sql
