from itertools import product
from typing import List

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from fake_useragent import UserAgent
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from dataclasses import dataclass
from bs4 import BeautifulSoup, Tag

user_agent = UserAgent()

retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=("GET")
)

session = requests.Session()
session.mount("https://", HTTPAdapter(max_retries=retry_strategy))


BASE_URL = "https://webscraper.io/"
HOME_URL = urljoin(BASE_URL, "test-sites/e-commerce/allinone/")


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

def get_home_products():

    try:
        response = session.get(HOME_URL, headers=HEADERS, timeout=10, verify=True)

        response.raise_for_status()

        headers = HEADERS.copy()
        headers["User-Agent"] = user_agent.random

        soup = BeautifulSoup(response.content, "html.parser")
        print(soup.prettify())
        return soup

    except requests.exceptions.RequestException as e:
        print(f"Error while executing the query: {e}")
        return None

    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

@dataclass
class Product:

    title: str
    description: str
    price: float
    rating: int
    num_of_reviews: int

def parse_single_product(product: Tag) -> Product:
    title = product.select_one(".title")["title"],
    description = product.select_one(".description").text

    price = float(product.select_one(".price").text.replace("$", "")),
    rating = int(product.select_one("[data-rating]")["data-rating"]),

    num_of_reviews = int(product.select_one(".review-count").text.split()[0])

def get_home_products() -> list[Product]:

    try:
        response = session.get(HOME_URL, headers=HEADERS, timeout=10, verify=True)
        response.raise_for_status()

        headers = HEADERS.copy()
        headers["User-Agent"] = user_agent.random

        soup = BeautifulSoup(response.content, "html.parser")
        products = soup.select(".card-body")

        return [parse_single_product(product) for product in products]


    except requests.exceptions.RequestException as e:
        print(f"Error executing the request: {e}")
        return None

    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def main():

    try:
        products = get_home_products()
        if products:
            print(f"The data has been successfully received and processed!\n")

            for index, product in enumerate(products, 1):
                print(f"{index}, {product}")
        else:
            print("Unable to retrieve data. Please check your connection or try again later.")

    except KeyboardInterrupt:
        print("The program was terminated by the user:")

    except Exception as e:
        print(f"Critical error: {e}")

    finally:
        session.close()

if __name__ == "__main__":
    main()