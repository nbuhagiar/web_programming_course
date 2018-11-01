#!/usr/bin/env python3

# ISetup tables in database

from sqlalchemy import create_engine
import os
import pandas as pd

def main():
    
    engine = create_engine(os.environ["DATABASE_URL"])
    books = pd.read_csv("books.csv")
    books.to_sql("book", con=engine)
    users = pd.DataFrame(columns=["username", "password"])
    users.to_sql("user", con=engine)
    reviews = pd.DataFrame(columns=["isbn", "username", "rating", "comment"])
    reviews.to_sql("review", con=engine)

if __name__ == "__main__":
    main()