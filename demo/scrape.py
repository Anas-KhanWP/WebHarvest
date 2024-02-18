import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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

    print(f"total elements => {len(availabily_check)}")

    if "Product availability" in availabily_check.text or "Disponibilité produit" in availabily_check.text:
        print("Element found")
        style_value = availabily_check.get("style")
        print(style_value)
        if style_value and ("display:none" in style_value or "display: none" in style_value):
            print(availabily_check.text)
            print("Product is available")
            return True
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


if __name__ == "__main__":
    driver = webdriver.Chrome()

    # Load the webpage
    driver.get("https://www.produceshop.fr/meubles-interieur/fauteuils-relax/fauteuils-inclinables/fauteuil-relax-inclinable-avec-repose-pieds-en-similicuir-design-aurora")

    # Assuming these functions are defined elsewhere in your code
    closepopup(driver)
    acceptcookie(driver)

    # Get the page source
    page_source = driver.page_source

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(page_source, "html.parser")

    availability = checkavailablity(soup)

    if availability:
        name = getname(soup)
        price = getprice(soup)