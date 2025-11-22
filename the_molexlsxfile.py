from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time
import os

def get_current_directory():
    """Get the current working directory."""
    return os.path.abspath(os.getcwd())

def setup_firefox_options(download_dir):
    """Set up Firefox options for downloading Excel files."""
    options = Options()
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.dir", download_dir)
    options.set_preference(
        "browser.helperApps.neverAsk.saveToDisk",
        "application/pdf;application/vnd.ms-excel;application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    options.add_argument("--headless")  
    return options

def find_excel_buttons(driver):
    """Find all buttons with 'excel' in their class."""
    return driver.find_elements(By.CSS_SELECTOR, "button[class*='excel']")

def click_button(driver, button):
    """Attempt to click on a button element."""
    try:
        driver.execute_script("arguments[0].scrollIntoView(true);", button)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", button)
        return True
    except Exception as e:
        print(f"Error when clicking: {e}")
        return False

def check_downloads(download_dir):
    excel_files = [f for f in os.listdir(download_dir) if f.endswith(('.xlsx', '.xls'))]
    recent_files = [f for f in excel_files if os.path.getctime(os.path.join(download_dir, f)) > time.time() - 60]
    return recent_files



def main():
    current_dir = get_current_directory()
    print(f"DE MOL CHALLENGE")
    print(f"Downloads will be saved to: {current_dir}")

    firefox_options = setup_firefox_options(current_dir)
    driver = webdriver.Firefox(options=firefox_options)

    try:
        url = "https://www.cim.be/nl/televisie?type=yearly_top_100&year=2021&region=north"
        print(f"Navigating to: {url}")
        driver.get(url)

        print("Waiting for page to load...")
        time.sleep(10)  
        buttons = driver.find_elements(By.TAG_NAME, "button")
        print(f"\nFound {len(buttons)} buttons on the page.")
        for i, button in enumerate(buttons, 1):
            print(f"Button {i} - Text: '{button.text}', Classes: {button.get_attribute('class')}")

        excel_buttons = find_excel_buttons(driver)
        if excel_buttons:
            print(f"\nFound Excel buttons: {len(excel_buttons)}")
            for button in excel_buttons:
                success = click_button(driver, button)
                if success:
                    print(f"Clicked on Excel button: {button.text}")
                    time.sleep(3) 
        else:
            print("No Excel buttons found.")

        recent_files = check_downloads(current_dir)
        if recent_files:
            newest_file = max(recent_files, key=lambda x: os.path.getctime(os.path.join(current_dir, x)))
            print(f"Success! Excel file downloaded: {newest_file}")
        else:
            print("No recent Excel files found. The mole has won this round!")

    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()