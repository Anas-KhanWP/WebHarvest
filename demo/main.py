from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



# Load the webpage
driver.get("https://www.produceshop.fr/meubles-interieur/fauteuils-relax/fauteuils-inclinables/fauteuil-relax-inclinable-avec-repose-pieds-en-similicuir-design-aurora")

# Assuming these functions are defined elsewhere in your code
closepopup()
acceptcookie()

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
