import requests


res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "iCodj2mDov5hoHYYVYKJlw", "isbns": "0380795272"})
deic=res.json()
print(deic)
print(deic["books"][0]["average_rating"])
