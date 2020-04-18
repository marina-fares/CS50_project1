import os
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgres://nauoudlmqbspyu:74b79990dbe93ff1b012f6757f51005d27830a1842441c5adae61aff9b050382@ec2-3-91-112-166.compute-1.amazonaws.com:5432/dfkq5v1f2772on") # database engine object from SQLAlchemy that manages connections to the database
                                                # DATABASE_URL is an environment variable that indicates where the database lives
db = scoped_session(sessionmaker(bind=engine))    # create a 'scoped session' that ensures different users' interactions with the

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    count=1
    for isbn,title,auther,year in reader:
        db.execute("INSERT INTO books (isbn,title,auther,year) VALUES (:i, :t,:a,:y)",
        {"i": isbn, "t": title, "a": auther, "y": year})
        print(f"Added Book {count}")
        count+=1
    db.commit()

if __name__ == "__main__":
    main()
