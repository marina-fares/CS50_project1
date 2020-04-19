
import os
import requests
from flask import Flask, session, render_template, request, flash, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)


#postgres://nauoudlmqbspyu:74b79990dbe93ff1b012f6757f51005d27830a1842441c5adae61aff9b050382@ec2-3-91-112-166.compute-1.amazonaws.com:5432/dfkq5v1f2772on
link="postgres://nauoudlmqbspyu:74b79990dbe93ff1b012f6757f51005d27830a1842441c5adae61aff9b050382@ec2-3-91-112-166.compute-1.amazonaws.com:5432/dfkq5v1f2772on"
# Check for environment variable
if link is None:
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine("postgres://nauoudlmqbspyu:74b79990dbe93ff1b012f6757f51005d27830a1842441c5adae61aff9b050382@ec2-3-91-112-166.compute-1.amazonaws.com:5432/dfkq5v1f2772on")
db = scoped_session(sessionmaker(bind=engine))


deic=[]


@app.route("/")
def home():
    return render_template("Home.html")

@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/register/home",methods=["POST"])
def storedata():
    fname=request.form.get("fname")
    lname=request.form.get("lname")
    email=request.form.get("email")
    passw=request.form.get("pass")
    if db.execute("select * from users where fname=:f and lname=:l",{'f':fname,"l":lname}).rowcount == 0:
        if db.execute("select * from users where email=:e",{'e':email}).rowcount==0:
            db.execute("INSERT INTO users (fname,lname,email,password) VALUES (:f, :l,:e,:p)",
            {"f": fname, "l": lname, "e": email, "p": passw})
            db.commit()
            return render_template("Home.html")
    else:
        return render_template("error.html",message="this email or username is used before please try again")
        

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/account",methods=["post"])
def getaccount():
    email=request.form.get("email")
    passw=int(request.form.get("password"))
    user=db.execute("select * from users where email=:e and password=:p",{'e':email,"p":passw}).fetchall()
    if len(user)==0:
        
        return render_template("error.html",message="email or password is wrong")
    else:
        return render_template("welcome.html",user=user)

@app.route("/welcome")
def welcome():
    return render_template("login.html",name=name)

@app.route("/search/<id>",methods=["post"])
def search(id):
    deic.clear()
    book=request.form.get("book")
    user=db.execute("select * from users where id=:i ",{'i':id}).fetchall()
    search_string= f"%{book}%"
    booklist=db.execute("SELECT * FROM books WHERE isbn LIKE :searching_string LIMIT 5",{"searching_string":search_string})
    if booklist is None:
        booklist=(db.execute("SELECT * FROM books WHERE isbn=:i OR author=:i OR title=:i",{"i":book}))
    for b in booklist:
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "iCodj2mDov5hoHYYVYKJlw", "isbns": b.isbn})
        deic.append(res.json())
    return render_template("welcome.html",booklist=deic,user=user)

@app.route("/book/<id>/<isbn>",methods=["post"])
def book(id,isbn):
    user=db.execute("select * from users where id=:i ",{'i':id}).fetchall()
    details=db.execute("SELECT * FROM books WHERE isbn=:isbn", {'isbn':isbn}).fetchall()
    reviews=db.execute("SELECT * FROM users INNER JOIN reviews ON users.id = reviews.userid").fetchall()
    
    return render_template("book.html",book=details,user=user,reviews=reviews)

@app.route("/review/<id>/<isbn>",methods=["post"])
def review(id,isbn):
    error=None
    user=db.execute("select * from users where id=:i ",{'i':id}).fetchall()
    details=db.execute("SELECT * FROM books WHERE isbn=:isbn", {'isbn':isbn}).fetchall()
    reviews=db.execute("SELECT * FROM users INNER JOIN reviews ON users.id = reviews.userid").fetchall()
    rate=float(request.form.get("rate"))
    commint=request.form.get("commint")
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "iCodj2mDov5hoHYYVYKJlw", "isbns": isbn})
    deic.append(res.json())
    if rate :
        if db.execute("SELECT * FROM reviews WHERE isbn=:isbn and userid=:id", {'isbn':isbn,'id':id}).rowcount==0:
            db.execute("INSERT INTO reviews (userid,isbn,rate,commint) VALUES (:u, :i,:r,:c)",
                {"u": id, "i": isbn, "r": rate, "c": commint})
            db.commit()
        else:
            return render_template("error.html",message="you already submit a review for this book")
    return render_template("book.html",book=details,user=user,reviews=reviews,error=error,deic=deic)

@app.route("/review/<id>/<isbn>/sub")
def subreview(id,isbn):
    user=db.execute("select * from users where id=:i ",{'i':id}).fetchall()
    details=db.execute("SELECT * FROM books WHERE isbn=:isbn", {'isbn':isbn}).fetchall()
    
    return render_template("review.html",book=details,user=user)

@app.route("/api/<isbn>")
def api(isbn):
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "iCodj2mDov5hoHYYVYKJlw", "isbns": isbn})
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")
    data = res.json()
    details=db.execute("SELECT * FROM books WHERE isbn=:isbn", {'isbn':isbn}).fetchall()
    return jsonify({
              "title": details[0].title,
              "author": details[0].author,
              "year": details[0].year,
              "isbn": isbn,
              "review_count": data["books"][0]["ratings_count"],
              "average_score": data["books"][0]["average_rating"]
          })



app.run(debug=True)

