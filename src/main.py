import sys
from selenium import webdriver
from scraper import WebScraper
from utils.file_handlers import write_products_to_csv
from utils.logger import setup_logger
from utils.selenium_utils import set_driver

logger = setup_logger(__name__)


def main():
    try:
        scraper = WebScraper()
        with webdriver.Chrome() as driver:
            set_driver(driver)
            write_products_to_csv(scraper.get_laptop_page_products())
            logger.info("Data successfully saved to 'products.csv' file")
    except KeyboardInterrupt:
        logger.warning("Program execution interrupted by user")
    except Exception as e:
        logger.critical(f"Critical error during program execution: {e}")
    finally:
        scraper.session.close()


if __name__ == "__main__":
    main()