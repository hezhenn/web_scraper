# 🕷️ Web Scraper Project

A Python web scraper for extracting product data from e-commerce websites. This project demonstrates advanced web
scraping techniques including **pagination handling**, **dynamic content parsing** with Selenium, **error management**,
and **data export** to CSV. Built with **requests**, **BeautifulSoup4**, **Selenium**, and Python's standard libraries.

## 🚀 Features

- **Product Data Extraction**: Collect comprehensive product information (title, description, price, rating, reviews)
- **Dynamic Content Handling**: Parse JavaScript-rendered content using Selenium
- **Configuration Price Parsing**: Extract prices for different product configurations
- **Pagination Support**: Automatically handle multi-page product listings
- **Error Handling**: Robust error management and logging system
- **CSV Export**: Save scraped data to structured CSV format
- **Session Management**: Efficient HTTP requests with session reuse

## 🛠️ Technology Stack

- **Python** - Core programming language
- **BeautifulSoup4** - HTML parsing library
- **Requests** - HTTP request handling
- **Selenium** - Dynamic content automation
- **Fake UserAgent** - User-Agent rotation for requests
- **Logging** - Application logging system
- **Dataclasses** - Modern Python data structures

## 📁 Project Structure

```
web_scraper/
│
├── .venv/                     # Virtual environment
│
├── src/                       # Source code directory
│   ├── main.py                # Entry point with WebDriver initialization
│   ├── scraper.py             # Web scraping logic with Selenium integration
│   ├── models.py              # Data models with additional_info field
│   └── utils/                 # Utility modules
│       ├── logger.py          # Logging configuration
│       ├── file_handlers.py   # File operations
│       └── selenium_utils.py  # WebDriver utilities
│
├── data/                      # Data output directory
│   └── products.csv           # Scraped products data
│
├── logs/                      # Application logs
│   └── parser.log             # Application log file
│
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
```

## 📦 Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd web_scraper
```

2. Create and activate virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## 🎯 Usage

Run from project root directory:

```bash
python -m src.main
```

## 📊 Output

- **Scraped Data**: Saved to `data/products.csv`
- **Application Logs**: Stored in `logs/parser.log`
- **Product Information**: Includes dynamic configuration prices

## 🔧 Educational Purpose

> 📦 This project is designed for **educational purposes**. Initially implemented in a **single file** for functionality
> testing, students are tasked with **structuring** the complete code by distributing it across appropriate
> **directories** and **modules** according to the defined project architecture.

## 📄 License

This project is created for educational purposes. Please use responsibly and respect website terms of service.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

---
