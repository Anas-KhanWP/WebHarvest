import csv
import time
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import tkinter as tk
from tkinter import filedialog


def select_file():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Open a file dialog for selecting a file
    file_path = filedialog.askopenfilename(title="Select file with URLs", filetypes=[("CSV files", "*.csv")])

    return file_path


def acceptcookie(soup):
    """
    Accepts the cookie on the webpage.

    Args:
    - soup: BeautifulSoup instance.

    Returns:
    None
    """
    try:
        accept_cookie = soup.find("button", class_="btn btn-primary accept-all-cookies")
        if accept_cookie:
            # You can add your cookie acceptance logic here
            pass
    except:
        pass


def closepopup(soup):
    """
    Closes a popup window on the webpage.

    Args:
    - soup: BeautifulSoup instance.

    Returns:
    None
    """
    try:
        close_button = soup.find('i', class_="material-icons", text="close")
        if close_button:
            time.sleep(5)  # Wait for 5 seconds
            # You can add your close popup logic here
            pass
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

    if availabily_check and (
            "Product availability" in availabily_check.text or "Disponibilité produit" in availabily_check.text):
        style_value = availabily_check.get("style")
        if style_value and ("display:none" in style_value or "display: none" in style_value):
            print(availabily_check.text)
            print("Product is available")
            return True
        else:
            print("Product is unavailable")
            estimated_time = soup.find("span", class_="product-info-value estimated-shipping-date")
            if estimated_time:
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


def gethtml(url):
    """
    Gets the HTML of the webpage.

    Args:
    - url: URL of the webpage.

    Returns:
    BeautifulSoup: Parsed HTML of the webpage.
    """
    try:
        # Send a GET request to the URL
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urlopen(req)
        # Parse the response content with BeautifulSoup
        soup = BeautifulSoup(response, "html.parser")
        return soup
    except:
        return None


def read_urls_from_csv(filename):
    urls = []
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            urls.append(row[0])  # Assuming URLs are in the first column
    return urls


if __name__ == "__main__":
    # Ask user to select CSV file
    csv_filename = select_file()
    if not csv_filename:
        print("No file selected. Exiting.")
        exit()

    # Read URLs from CSV file
    urls = read_urls_from_csv(csv_filename)

    for url in urls:
        print(url)
        # Get the HTML of the webpage
        soup = gethtml(url)

        if soup:
            # closepopup(soup)
            # acceptcookie(soup)

            # Add your logic for variant selection here if needed

            # Extract information
            name = getname(soup)
            price = getprice(soup)
            availability = checkavailablity(soup)

            # Write the extracted information to the CSV file
            with open('output_23.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([name, url, '', availability, price])

        else:
            print(f"Failed to get HTML for URL: {url}")
