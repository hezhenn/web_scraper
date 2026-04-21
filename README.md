# web_scraper
A Python web scraper for extracting product data from e-commerce websites. This project demonstrates web scraping techniques including pagination handling, error management, and data export to CSV. Built with requests, BeautifulSoup4, and Python's standard libraries.

## 1. Project Description

> The project implements a **web scraper** to collect data on **products** from [an online store](https://webscraper.io/test-sites)
> using the **Python** programming language and the **requests**, **BeautifulSoup4**, and **Selenium** libraries.

### 📦 Key Features:

- Collection of product data (**name**, **description**, **price**, **rating**, **number of reviews**)
- Handling of **pagination** to retrieve all available products
- **Dynamic parsing** of prices for various product **configurations**
- Handling **errors** and **logging** the scraping process
- **Saving** the retrieved data to a **CSV** file
- Using **sessions** for efficient **HTTP** requests

### 📦 Technology stack:

- `Python` - primary programming language
- `BeautifulSoup4` - third-party library for **HTML** parsing
- `requests` - third-party library for executing **HTTP** requests
- `Selenium` - third-party library for working with **dynamic content**
- `logging` - built-in library for **logging** scraper activity
- `dataclasses` - built-in library for convenient **data storage** of product information

### 📦 Main components:

- `Product` - **class** for storing **information** about a **product**
- `WebScraper` - **class** for the main scraping logic
- `parse_single_product` - a handler function for a **single product**
- `parse_hdd_block_prices` - a function for retrieving **dynamic prices** for configurations
- `scrape_products` - a function for **retrieving products** from all pages
- `get_num_pages` - a function for determining the **number