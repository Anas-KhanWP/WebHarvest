import time 
from bs4 import BeautifulSoup

def checkavailablity(soup):
    """
    Checks the availability of a product on the webpage.

    Args:
    - soup: BeautifulSoup instance.

    Returns:
    str: Availability of product.
    """
    availability_check = soup.find("span", class_="product-info-label stock-date")

    if "Product availability" in availability_check.text or "Disponibilité produit" in availabily_check.text:
        style_value = availability_check.get("style")
        if style_value and ("display:none" in style_value or "display: none" in style_value):
            print(availability_check.text)
            print("Product is available")
            return "Available"
        else:
            print("Product is unavailable")
            estimated_time = soup.find("span", class_="product-info-value.estimated-shipping-date")

            time_ = estimated_time.text
            return time_
    else:
        print("no element")
        return False
    
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
    str: HTML of the webpage.
    """
    try:
        # Get the page source
        page_source = driver.page_source

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(page_source, "html.parser")
        return soup
    except:
        print("HTML not found retrying...")
        gethtml(driver)

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


def selectvariant(driver, url, row, result_corpus):
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

            if row['Color'] != _variants or row['Availability'] != availabilities or row['Price'] != prices:
                result_corpus.loc[len(result_corpus)] = [
                    url,
                    _variants, 
                    availabilities, 
                    prices
                ]

            else:
                result_corpus.loc[len(result_corpus)] = [
                    url, 
                    row['Color'], 
                    row['Availability'], 
                    row['Price']
                ]

        else:
            soup = gethtml(driver)
            availability = checkavailablity(soup)
            price = getprice(soup)
            variant = "No Vairant"

            if row['Price'] != price or row['Availability'] != availability or row['Color'] != variant:
                result_corpus.loc[len(result_corpus)] = [url, variant, availability, price]

            else:
                result_corpus.loc[len(result_corpus)] = [
                    url,
                    row['Color'],
                    row['Availability'],
                    row['Price']
                ]
                
    except Exception as e:
        print(f"Error occurred: {e}")

def scraper(driver, url, row, result_corpus):
    print(url)
    driver.get(url)
    time.sleep(2)
    selectvariant(driver, url, row, result_corpus)
#     pass
