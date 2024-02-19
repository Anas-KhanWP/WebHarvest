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
            return True
        else:
            print("Product is unavailable")
            estimated_time = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, "product-info-value.estimated-shipping-date"))
            )
            time_ = estimated_time.text
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
        return None


def totaloptions(options):
    # Count the number of options
    options_count = str(len(options))
    print("Total options => ", options_count)
    return options_count


def getdropdown(driver):
    variants_dropdown = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "form-control.form-control-select"))
    )

    # Get all the options within the select element
    options = Select(variants_dropdown).options
    total_variants = len(options)
    print(f"Total options => {total_variants}")
    return options, variants_dropdown, total_variants


def selectvariant(driver, url):
    """
    This function selects a variant for a product on a webpage. It iterates through all the options in the variants dropdown and extracts the product name, price, and availability for each option. The function also records the selected option in a CSV file.

    Args:
        driver (selenium.webdriver.remote.webdriver.WebDriver): A Selenium WebDriver instance.
        url (str): The URL of the product page.

    Returns:
        None

    Raises:
        Exception: If an error occurs while selecting the variant.
    """
    try:
        options, variants_dropdown, total_variants = getdropdown(driver)

        # Get aria-label attribute of select element
        aria_label = variants_dropdown.get_attribute("aria-label")
        print(f"Select Aria Label: {aria_label}")

        option_texts = []
        option_vals = []
        option_titles = []

        for index in range(total_variants):  # Iterate through all options
            # Get the text, value, and title of the option
            option_text = options[index].text
            option_texts.append(option_text)
            option_value = options[index].get_attribute("value")
            option_vals.append(option_value)
            option_title = options[index].get_attribute("title")
            option_titles.append(option_title)

        with open('output_2.csv', mode='a', newline='') as file:
            writer = csv.writer(file)

            # Iterate over the lists simultaneously using zip
            for option_text, option_val, option_title in zip(option_texts, option_vals, option_titles):
                if '(' in option_text:
                    # Extract the option text without the additional information
                    clean_option_text = option_text.split('(')[0].strip()
                    print(f"Option text: {clean_option_text}, Value: {option_val}, Title: {option_title}")

                    new_url = f"{url}#/{option_val}-{aria_label}-{option_title}"
                    print(new_url)
                    driver.get(new_url)
                    time.sleep(2)  # Wait for 5 seconds
                    driver.refresh()
                    time.sleep(5)

                    # Get the page source
                    soup = gethtml(driver)

                    availability = checkavailablity(soup)
                    print(availability)

                    # if availability:
                    name = getname(soup)
                    price = getprice(soup)

                else:
                    print(f"Option text: {option_text}, Value: {option_val}, Title: {option_title}")
                    new_url = f"{url}#/{option_val}-{aria_label}-{option_title}"
                    print(new_url)
                    driver.get(new_url)
                    time.sleep(2)  # Wait for 5 seconds
                    driver.refresh()
                    time.sleep(5)

                    # Get the page source
                    soup = gethtml(driver)

                    availability = checkavailablity(soup)
                    print(availability)

                    # if availability:
                    name = getname(soup)
                    price = getprice(soup)

                # Write the extracted information to the CSV file
                writer.writerow(
                    [
                        name,
                        new_url,
                        option_title,
                        availability,
                        price
                    ]
                )

        print("I am done")
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
        exit()

    # Read URLs from CSV file
    urls = read_urls_from_csv(csv_filename)

    for url in urls:
        print(url)
        # Load the webpage
        driver.get(url)

        closepopup(driver)
        acceptcookie(driver)

        selectvariant(driver, url)
