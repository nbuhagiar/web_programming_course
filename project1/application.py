import os

from flask import Flask, session, render_template, request, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# Set up Goodreads API key
key = os.getenv("API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    """
    Home page.
    """
    return render_template("index.html")

@app.route("/register/")
def register():
    """
    New User registration page.
    """
    return render_template("register.html")

@app.route("/login/")
def login():
    """
    User login page.
    """
    return render_template("login.html")

@app.route("/search_results", methods=["GET", "POST"])
def search_results():
    """
    Search results page.
    """

    title = request.form.get("title")
    author = request.form.get("author")
    isbn = request.form.get("isbn")
    results = db.execute("""
        SELECT *
        FROM book
        WHERE LOWER(title) LIKE '%' || LOWER(:title) || '%'
        AND LOWER(author) LIKE '%' || LOWER(:author) || '%'
        AND LOWER(isbn) LIKE '%' || LOWER(:isbn) || '%'
        """, {"title": title, "author": author, "isbn": isbn}).fetchall()
    return render_template("search_results.html", results=results)

@app.route("/book/<int:book_index>/")
def book(book_index):
    """
    Book page.
    """
    book = db.execute("SELECT * FROM book WHERE index = :index", 
        {"index": book_index}).fetchone()
    reviews = db.execute("SELECT * FROM review where isbn = :isbn", 
        {"isbn": book.isbn}).fetchall()
    resp = requests.get("https://www.goodreads.com/book/review_counts.json", 
        params=dict(key=key, isbns=book.isbn)).json()
    mean_rating = resp["books"][0]["average_rating"]
    num_ratings = resp["books"][0]["ratings_count"]
    return render_template("book.html",
        book=book,
        reviews=reviews,
        mean_rating=mean_rating,
        num_ratings=num_ratings)

@app.route("/api/<isbn>/")
def book_api(isbn):
    """
    Book API result page.
    """
    
    book = db.execute("SELECT * FROM book WHERE isbn = :isbn", 
        {"isbn": isbn}).fetchone()
    if not book:
        return jsonify({"error": "Invalid ISBN"}), 404
    else:
        return jsonify({
            "title": book.title,
            "author": book.author,
            "year": book.year,
            "isbn": book.isbn
            })
