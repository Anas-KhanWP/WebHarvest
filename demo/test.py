import requests
from bs4 import BeautifulSoup

# Define the URL of the webpage you want to scrape
url = 'https://www.produceshop.fr/bricolage/barbecues/barbecues-portatifs-au-charbon-de-bois/barbecue-pliable-portable-et-pratique-pour-barbecue-en-plein-air-beech'


print("Sending request")
# Send an HTTP GET request to the URL
response = requests.get(url)
print(f"Response => {response.status_code}")

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Now you can use BeautifulSoup to extract specific information from the HTML
    # For example, let's extract the title of the webpage
    title = soup.title
    print("Title:", title.text)

    # You can also find specific elements by their tags, classes, or IDs
    # For example, let's find all the links on the webpage
    links = soup.find_all('a')
    print("Links:")
    for link in links:
        print(link.get('href'))
else:
    # If the request was not successful, print an error message
    print("Error: Failed to retrieve webpage. Status code:", response.status_code)
