import requests
import csv
import logging
import sys
from bs4 import BeautifulSoup, Tag
from urllib.parse import urljoin
from fake_useragent import UserAgent
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from dataclasses import dataclass, fields, astuple
from selenium import webdriver
from selenium.webdriver.common.by import By


logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s]: %(message)s",
    handlers=[
        logging.FileHandler("parser.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ]
)

@dataclass
class Product:
    title: str
    description: str
    price: float
    rating: int
    num_of_reviews: int
    additional_info: dict[str, float]

PRODUCT_FIELDS = [field.name for field in fields(Product)]

_driver: webdriver.WebDriver | None = None


def get_driver() -> webdriver.Chrome:
    return _driver


def set_driver(new_driver: webdriver.WebDriver) -> None:
    global _driver
    _driver = new_driver


user_agent = UserAgent()

retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[
        429,
        500,
        502,
        503,
        504
    ],
    allowed_methods=["GET"]
)

session = requests.Session()
session.mount("https://", HTTPAdapter(max_retries=retry_strategy))
session.mount("http://", HTTPAdapter(max_retries=retry_strategy))


BASE_URL = "https://webscraper.io/"

HOME_URL = urljoin(BASE_URL, "test-sites/e-commerce/allinone/")
LAPTOP_URL = urljoin(BASE_URL, "test-sites/e-commerce/static/computers/laptops/")

HEADERS = {
    'User-Agent': user_agent.random,
    'Accept': (
        'text/html,application/xhtml+xml,application/xml;'
        'q=0.9,image/webp,*/*;q=0.8'
    ),
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

def get_home_products() -> list[Product]:
    try:
        response = session.get(
            HOME_URL,
            headers=HEADERS,
            timeout=10,
            verify=True
        )

        response.raise_for_status()

        headers = HEADERS.copy()
        headers["User-Agent"] = user_agent.random

        soup = BeautifulSoup(response.content, 'html.parser')
        products = soup.select(".card-body")

        return [parse_single_product(product) for product in products]

    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Error while executing the query: {e}")
        return None
    except Exception as e:
        logging.warning(f"⚠️ Unexpected error: {e}")
        return None

def parse_single_product(product: Tag) -> Product:

    hdd_prices = parse_hdd_block_prices(product)

    return Product(
        title = product.select_one(".title")["title"],
        description = product.select_one(".description").text,
        price = float(product.select_one(".price").text.replace("$", "")),
        rating = int(product.select_one("[data-rating]")["data-rating"]),
        num_of_reviews = int(product.select_one(".review-count").text.split()[0]),
        additional_info = {"hdd_prices": hdd_prices}
    )

def get_laptop_page_products() -> list[Product]:
    try:
        response = session.get(
            LAPTOP_URL,
            headers=HEADERS,
            timeout=10,
            verify=True
        )
        response.raise_for_status()

        first_page_soup = BeautifulSoup(response.content, 'html.parser')

        all_products = get_single_page_products(first_page_soup)

        num_pages = get_num_pages(first_page_soup)
        logging.info(f"Total number of pages found: {num_pages}")
        logging.info(f"Start parsing page 1 from: {len(all_products)}")

        for page_num in range(2, num_pages + 1):
            logging.info(f"Start parsing the page {page_num} of {num_pages}")

            response = session.get(
                LAPTOP_URL,
                headers=HEADERS,
                params={"page": page_num},
                timeout=10,
                verify=True
            )
            response.raise_for_status()

            next_page_soup = BeautifulSoup(response.content, 'html.parser')
            all_products.extend(get_single_page_products(next_page_soup))

        logging.info(f"Total number of items found: {len(all_products)}")
        return all_products

    except requests.exceptions.RequestException as e:
        print(f"❌ Error while executing the query: {e}")
        return None
    except Exception as e:
        print(f"⚠️ Unexpected error: {e}")
        return None

def get_num_pages(page_soup: Tag) -> int:

    pagination = page_soup.select_one(".pagination")

    if pagination is None:
        return 0

    return int(pagination.select("li")[-2].text)

def get_single_page_products(page_soup: Tag) -> list[Product]:

    products = page_soup.select(".card-body")
    return [parse_single_product(product) for product in products]

def parse_hdd_block_prices(product_soup: Tag) -> dict[str, float]:

    try:
        absolute_url = urljoin(BASE_URL, product_soup.select_one(".title")["href"])

        driver = get_driver()
        driver.get(absolute_url)

        swatches - driver.find_element(By.CLASS_NAME, "swatches")
        buttons = driver.find_elements(By.TAG_NAME, "button")

        prices = {}

        for button in buttons:
            if not button.get_property("disabled"):
                button.click()

                price_text = driver.find_element(By.CLASS_NAME, "price").text
                price_value = float(price_text.replace("$", ""))

                config_name = button.get_property("value")

                prices[config_name] = price_value

                logging.info(f"HDD Configuration '{config_name}' -> ${price_value}")

        return prices

    except Exception as e:
        logging.warning(f"Error parsing HDD blocks: {e}")
        return {}

def write_products_to_csv(products: list[Product]) -> None:

    with open("products.csv", "w", newline="", encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(PRODUCT_FIELDS)
        writer.writerows([astuple(product) for product in products])


def main():
    try:

        with webdriver.Chrome() as driver:
            set_driver(driver)

            products = get_laptop_page_products()
            write_products_to_csv(products)

            logging.info(f"Successfully processed {len(products)} products with configurations")

    except KeyboardInterrupt:
        logging.warning("\n🛑 The user has terminated the program")
    except Exception as e:
        logging.critical(f"❌ Critical error: {e}")
    finally:
        session.close()
        logging.info("Application resources successfully released")


if __name__ == "__main__":
    main()