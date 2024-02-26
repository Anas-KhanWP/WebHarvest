import pandas as pd
import gspread
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from credentials import config
from mailer import send_email
import importlib.util
from KeyValue import redirectpath
import time
# Import website-specific scripts here, e.g., from websites.candyshop import scrape_candyshop

# Global DataFrame to store data from Google Sheet
global_df = pd.DataFrame()
scraper_functions = {}

def read_data_from_spreadsheet():
    global global_df
    gc = gspread.service_account(filename=config.SERVICE_ACCOUNT_FILE)
    sh = gc.open_by_url(config.SPREADSHEET_URL)
    worksheet = sh.get_worksheet(0)
    global_df = pd.DataFrame(worksheet.get_all_records())

def init_selenium_driver():
    options = Options()
    options.add_argument('--headless')  # Run Chrome in headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def update_spreadsheet_with_dataframe(df):
    gc = gspread.service_account(filename=config.SERVICE_ACCOUNT_FILE)
    sh = gc.open_by_url(config.SPREADSHEET_URL)
    worksheet = sh.get_worksheet(0)
    # Clear the worksheet and update with new DataFrame
    worksheet.clear()
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())


def load_scraper_functions(redirectpath):
    for base_url, script_path in redirectpath.items():
        module_name = script_path.replace('/', '.').replace('.py', '')
        spec = importlib.util.spec_from_file_location(module_name, script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        # Store the scraper function reference instead of the script path
        scraper_functions[base_url] = module.scraper
        print(f"Scraper Functions => {scraper_functions}")
        

def trigger_website_scripts(driver, result_corpus):
    # Load all scraper functions based on the redirectpath
    load_scraper_functions(redirectpath)
    count = 0  
    # Now iterate through the DataFrame and call the respective scraper function
    for index, row in global_df.iterrows():
        url = row['Lien fournisseur']
        urlCheck = str(row['Lien fournisseur'])
        for base_url in scraper_functions:
            if base_url in urlCheck:
                print(f"Row => {row}")
                # Directly call the scraper function for the URL
                scraper_functions[base_url](driver, url, row, result_corpus)
                # updatedRow =scraper_functions[base_url](driver, url,row)
                # if updatedRow != row :
                #     # do  change here  :)
                #     pass
                count+=1
                break  # Break after finding and calling the scraper function
    print("this many links triggered===>",count)
    
    
def main_controller():
    
    # Creating a corpus to store the results!
    result_corpus = pd.DataFrame(
        columns = [
            'url',
            '_variants',
            'availabilities',
            'prices'
        ]
    )

    read_data_from_spreadsheet()
    driver = init_selenium_driver()
    print(global_df.head())
    print("driver is launched and good to use :)")
    trigger_website_scripts(driver, result_corpus)
    # After all scripts have run and potential updates
    # update_spreadsheet_with_dataframe(global_df)
    driver.quit()

    # Save the DataFrame to an Excel file
    result_corpus.to_excel('result_corpus.xlsx', index=False)
    

if __name__ == "__main__":
    main_controller()
