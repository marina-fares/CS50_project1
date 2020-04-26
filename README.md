# Book review website

#Description

you can register for your website and then log in using your username and password. then you will be able to search for books, leave reviews for individual books, and see the reviews made by other people.<br/>

#files<br/>
.
├── static/css                   # all css files<br/>
│    ├── book.css<br/>
│    ├── home.css<br/>
│    ├── login.css<br/>
│    ├── register.css<br/>
│    ├── welcome.css<br/>
├── templates                    # all html files   <br/>                              
│    ├── layout.html<br/>
│    ├── error.html<br/>
│    ├── book.html<br/>
│    ├── home.html<br/>
│    ├── login.html<br/>
│    ├── register.html<br/>
│    ├── welcome.html<br/>
│    ├── review.html<br/>
├── application.py               # flask application file<br/> 
├── books.csv                    # data of 5000 book contain isbn,title,author,year<br/>
├── data.py                      # read data from csv file and store it in database<br/>
├── import.py                    # read data from goodrads website<br/>
├── requirements.txt<br/>
└── README.md<br/>
