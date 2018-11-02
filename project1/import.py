#!/usr/bin/env python3

# Setup book table in database

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import csv

def main():
    
    engine = create_engine(os.getenv("DATABASE_URL"))
    db = scoped_session(sessionmaker(bind=engine))
    f = open("books.csv")
    reader = csv.reader(f)
    next(reader)
    for isbn, title, author, year in reader:
        db.execute("""
            INSERT INTO book (isbn, title, author, year)
            VALUES (:isbn, :title, :author, :year)
            """, dict(isbn=isbn, title=title, author=author, year=year))
        db.commit()

if __name__ == "__main__":
    main()