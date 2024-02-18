from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def acceptcookie(driver):
    accept_cookie = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//button[@class='btn btn-primary accept-all-cookies']"))
    )

    if accept_cookie:
        accept_cookie.click()


def closepopup(driver):
    close_button = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//i[@class="material-icons"][text()="close"]'))
    )

    if close_button:
        close_button.click()


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

# Find the element with the specified class name
elements = soup.find_all("span", class_="product-info-label stock-date")

print(f"total elements => {len(elements)}")

for e in elements:
    if "Product availability" in e.text or "Disponibilité produit" in e.text:
        print("Element found")
        style_value = e.get("style")

        print(style_value)

        if style_value and ("display:none" in style_value or "display: none" in style_value):
            print(e.text)

    else:
        print("no element")
