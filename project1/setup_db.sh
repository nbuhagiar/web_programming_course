#!/bin/sh

# Create book, user, and review tables in database and load
# 'books.csv' into book table

psql -f create.sql $DATABASE_URL
./import.py