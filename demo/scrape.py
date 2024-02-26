import csv
import time
import tkinter as tk
from tkinter import filedialog
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.common.exceptions import StaleElementReferenceException


def select_file():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Open a file dialog for selecting a file
    file_path = filedialog.askopenfilename(title="Select file with URLs", filetypes=[("CSV files", "*.csv")])

    return file_path


def acceptcookie(driver):
    """
    Accepts the cookie on the webpage.

    Args:
    - driver: Selenium WebDriver instance.

    Returns:
    None
    """
    try:
        accept_cookie = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//button[@class='btn btn-primary accept-all-cookies']"))
        )

        if accept_cookie:
            accept_cookie.click()
    except:
        pass


def closepopup(driver):
    """
    Closes a popup window on the webpage.

    Args:
    - driver: Selenium WebDriver instance.

    Returns:
    None
    """
    try:
        close_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//i[@class="material-icons"][text()="close"]'))
        )

        if close_button:
            time.sleep(5)  # Wait for 5 seconds
            close_button.click()
    except:
        pass


def checkavailablity(soup):
    """
    Checks the availability of a product on the webpage.

    Args:
    - soup: BeautifulSoup instance.

    Returns:
    bool: True if product is available, False otherwise.
    """
    availabily_check = soup.find("span", class_="product-info-label stock-date")

    if "Product availability" in availabily_check.text or "Disponibilité produit" in availabily_check.text:
        style_value = availabily_check.get("style")
        if style_value and ("display:none" in style_value or "display: none" in style_value):
            print(availabily_check.text)
            print("Product is available")
            return "Available"
        else:
            print("Product is unavailable")
            estimated_time = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, "product-info-value.estimated-shipping-date"))
            )
            time_ = estimated_time.text
            print(f"Estimated time => {time_}")
            return time_
    else:
        print("no element")
        return False


def getname(soup):
    """
    Gets the name of a product from the webpage.

    Args:
    - soup: BeautifulSoup instance.

    Returns:
    str: Product name if found, None otherwise.
    """
    try:
        name = soup.find("h1", class_="h1").text
        print(f"Product Name => {name}")
        return name
    except:
        print("Name not found")
        return None


def getprice(soup):
    """
    Gets the price of a product from the webpage.

    Args:
    - soup: BeautifulSoup instance.

    Returns:
    str: Product price if found, None otherwise.
    """
    try:
        _price = soup.find("span", class_="current-price-value")
        price_val = _price.get("content")
        print(f"Product Price => {price_val}")
        return price_val
    except:
        return None


def gethtml(driver):
    """
    Gets the HTML of the webpage.

    Args:
    - driver: Selenium WebDriver instance.

    Returns:
    str: HTML of the webpage if found, None otherwise.
    """
    try:
        # Get the page source
        page_source = driver.page_source

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(page_source, "html.parser")
        return soup
    except:
        print("HTML not found, Retrying...")
        gethtml(driver)


def totaloptions(options):
    # Count the number of options
    options_count = str(len(options))
    print("Total options => ", options_count)
    return options_count


def getdropdown(driver):
    try:
        soup = gethtml(driver)
        # Find the dropdown element
        variants_dropdown = soup.find(class_="form-control form-control-select")
        if variants_dropdown:
            # Find all option elements within the dropdown
            options = variants_dropdown.find_all('option')
            total_variants = len(options)
            print(f"Total options => {total_variants}")
            return options, variants_dropdown, total_variants
        else:
            print("Dropdown not found")
            return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def selectvariant(driver, url):
    try:
        dropdown_data = getdropdown(driver)

        if dropdown_data:  # Check if dropdown_data is not False
            options, variants_dropdown, total_variants = dropdown_data
            aria_label = variants_dropdown["aria-label"]

            option_vals = []
            _variants = []
            availabilities = []
            prices = []

            for index in range(total_variants):
                option_value = options[index]['value']
                option_vals.append(option_value)
                variant = options[index]['title']
                _variants.append(variant)

            for option_val, variant in zip(option_vals, _variants):
                new_url = f"{url}#/{option_val}-{aria_label}-{variant}"
                driver.get(new_url)
                # time.sleep(0.5)
                driver.refresh()
                # time.sleep(2)

                soup = gethtml(driver)

                availability = checkavailablity(soup)
                availabilities.append(availability)
                price = getprice(soup)
                prices.append(price)

            corpus.loc[len(corpus)] = [url, _variants, availabilities, prices]

        else:
            soup = gethtml(driver)
            availability = checkavailablity(soup)
            price = getprice(soup)
            variant = "No Vairant"

            corpus.loc[len(corpus)] = [url, variant, availability, price]

    except Exception as e:
        print(f"Error occurred: {e}")


def read_urls_from_csv(filename):
    urls = []
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            urls.append(row[0])  # Assuming URLs are in the first column
    return urls


if __name__ == "__main__":
    # Create Chrome options
    chrome_options = Options()

    # Add options to make Chrome run faster
    chrome_options.add_argument("--disable-extensions")  # Disable extensions
    chrome_options.add_argument("--disable-gpu")  # Disable GPU usage
    chrome_options.add_argument("--no-sandbox")  # Disable sandbox
    chrome_options.add_argument("--disable-dev-shm-usage")  # Disable shared memory usage
    chrome_options.add_argument("--dns-prefetch-disable")  # Disable DNS prefetching
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")  # Disable VizDisplayCompositor
    chrome_options.add_argument("--disable-site-isolation-trials")  # Disable site isolation trials
    chrome_options.add_argument("--ignore-certificate-errors")  # Ignore certificate errors
    chrome_options.add_argument("--ignore-ssl-errors")  # Ignore SSL errors

    driver = webdriver.Chrome(options=chrome_options)

    # Ask user to select CSV file
    csv_filename = select_file()
    if not csv_filename:
        print("No file selected. Exiting.")
        driver.quit()
        exit()

    # Read URLs from CSV file
    urls = read_urls_from_csv(csv_filename)

    # Assuming you have initialized an empty DataFrame for your corpus
    corpus = pd.DataFrame(columns=['url', '_variants', 'availabilities', 'prices'])

    for url in urls:
        print(url)
        # Load the webpage
        driver.get(url)

        # closepopup(driver)
        # acceptcookie(driver)

        selectvariant(driver, url)

    print(f"Corpus size => {len(corpus)}")
    print(f"Corpus => {corpus}")
    driver.quit()

    # After calling the function for all necessary URLs and rows, you can save the corpus to a CSV file
    corpus.to_csv('corpus.csv', index=False)
