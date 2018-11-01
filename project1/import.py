#!/usr/bin/env python3

# Import 'books.csv' into database

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import os
import pandas as pd

db = SQLAlchemy()

class Book(db.Model):

    __tablename__ = "book"
    isbn = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)

def main():
    
    engine = create_engine(os.environ["DATABASE_URL"])
    books = pd.read_csv("books.csv")
    books.to_sql("book", con=engine, if_exists="append")

if __name__ == "__main__":
    main()