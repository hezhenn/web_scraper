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

PRODUCT_FIELDS = [field.name for field in fields(Product)]

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
    return Product(
        title = product.select_one(".title")["title"],
        description = product.select_one(".description").text,
        price = float(product.select_one(".price").text.replace("$", "")),
        rating = int(product.select_one("[data-rating]")["data-rating"]),
        num_of_reviews = int(product.select_one(".review-count").text.split()[0])
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

def write_products_to_csv(products: list[Product]) -> None:

    with open("products.csv", "w", newline="", encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(PRODUCT_FIELDS)
        writer.writerows([astuple(product) for product in products])


def main():
    try:

        write_products_to_csv(get_laptop_page_products())
        print("✅ Data successfully saved to the 'products.csv'")

    except KeyboardInterrupt:
        logging.warning("\n🛑 The user has terminated the program")
    except Exception as e:
        logging.critical(f"❌ Critical error: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    main()