# Books Scraper 📚🖥️

## Overview
This project is a Python web scraper that extracts book information from the website [Books to Scrape](http://books.toscrape.com/).  
It collects:

- Book titles
- Prices

And saves the results in a JSON file for easy analysis.

---

## Features
- Fetches live HTML content using `requests`
- Parses structured HTML with **BeautifulSoup**
- Extracts multiple book entries from a page
- Saves output to `books.json`

---

## Requirements
- Python 3.8+
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)
- [requests](https://pypi.org/project/requests/)

Install dependencies:

```powershell
py -m pip install beautifulsoup4 requests
