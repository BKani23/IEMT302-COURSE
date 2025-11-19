import requests
from bs4 import BeautifulSoup
import json

# URL to scrape
url = "http://books.toscrape.com/"

# Fetch the page
response = requests.get(url)
response.raise_for_status()  # stops if request failed

# Parse HTML
soup = BeautifulSoup(response.text, "html.parser")

# Extract all book titles and prices
books = []
for book in soup.select("article.product_pod"):
    title = book.h3.a["title"]
    price = book.find("p", class_="price_color").text
    books.append({"title": title, "price": price})

# Save to JSON
with open("books.json", "w", encoding="utf-8") as f:
    json.dump(books, f, indent=4)

print(f"Extracted {len(books)} books. Saved to books.json")