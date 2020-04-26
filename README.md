# Book review website

#Description

you can register for your website and then log in using your username and password. then you will be able to search for books, leave reviews for individual books, and see the reviews made by other people.

#files
.
├── static/css                   # all css files<br/>
│    ├── book.css<br/>
│    ├── home.css<br/>
│    ├── login.css<br/>
│    ├── register.css<br/>
│    ├── welcome.css<br/>
├── templates                    # all html files                                 
│    ├── layout.html
│    ├── error.html
│    ├── book.html
│    ├── home.html
│    ├── login.html
│    ├── register.html
│    ├── welcome.html
│    ├── review.html
├── application.py               # flask application file 
├── books.csv                    # data of 5000 book contain isbn,title,author,year
├── data.py                      # read data from csv file and store it in database
├── import.py                    # read data from goodrads website
├── requirements.txt
└── README.md
