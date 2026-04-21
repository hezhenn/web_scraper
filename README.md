# web_scraper
A Python web scraper for extracting product data from e-commerce websites. This project demonstrates web scraping techniques including pagination handling, error management, and data export to CSV. Built with requests, BeautifulSoup4, and Python's standard libraries.

1. Project Description
This project implements a web scraper to collect product data from an online store using the Python programming language and the requests, BeautifulSoup4, and Selenium libraries.

📦 Key Features:
Collection of product data (name, description, price, rating, number of reviews)
Pagination handling to retrieve all available products
Dynamic parsing of prices for different product configurations
Error handling and logging of the scraping process
Saving retrieved data to a CSV file
Using sessions for efficient HTTP requests
📦 Technology stack:
Python - primary programming language
BeautifulSoup4 - third-party library for HTML parsing
requests - third-party library for making HTTP requests
Selenium - third-party library for working with dynamic content
logging - built-in library for logging scraper activity
dataclasses - built-in library for convenient storage of product data
📦 Main components:
Product - a class for storing product information
WebScraper - a class for the main scraping logic
parse_single_product - a handler function for a single product
parse_hdd_block_prices - a function for retrieving dynamic prices for product configurations
scrape_products - a function for retrieving products from all pages
get_num_pages - a function for determining the number of pages during pagination
write_products_to_csv - a function for exporting data to a CSV file

✔ Структура проєкту
web_scraper_group_6/
│
├── .venv/                     # Віртуальне оточення Python
│
├── src/                       # Основна директорія з вихідним кодом
│   ├── main.py                # Основний файл з точкою входу
│   ├── scraper.py             # Логіка скрапінгу
│   ├── models.py              # Моделі даних
│   └── utils/                 # Допоміжні модулі
│       ├── logger.py          # Налаштування логування
│       ├── file_handlers.py   # Робота з файлами
│       └── selenium_utils.py  # Selenium WebDriver утиліти
│
├── data/                      # Директорія для збережених даних
│   └── products.csv           # Експортовані дані
│
├── logs/                      # Логи роботи скрапера
│   └── parser.log
│
├── requirements.txt           # Залежності проекту
└── README.md                  # Документація проекту