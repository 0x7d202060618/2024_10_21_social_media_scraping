from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Initialize Chrome options
options = Options()
options.add_argument("start-maximized")

# Function to extract followers count from a Facebook profile
def get_facebook_followers(profile_url):
    # Start the WebDriver
    driver = webdriver.Chrome(options=options)
    
    try:
        # Open the Facebook profile page
        driver.get(profile_url)
        time.sleep(2)  # Let the page load
        
        # Close any dialog box if it appears (e.g., a pop-up asking to log in)
        try:
            close_button = driver.find_element(By.CSS_SELECTOR, '[aria-label="Close"]')
            close_button.click()
            print("Close button clicked.")
            time.sleep(1)  # Wait to ensure the dialog is closed
        except Exception as e:
            print(f"No dialog to close or issue closing dialog: {e}")

        # Now, locate the followers element
        try:
            followers_element = driver.find_element(By.CSS_SELECTOR, 'a[href*="followers"]')
            
            # Extract and print the text (e.g., "51M followers")
            followers_text = followers_element.text
            followers_count = followers_text.split()[0]  # Extract just the numeric part (e.g., '51M')
            
            print(f"Followers Count: {followers_count}")
        except Exception as e:
            print(f"Error extracting followers count: {e}")
    
    finally:
        # Close the driver
        driver.quit()

# Example usage:
profile_url = input("Enter the Facebook profile URL: ")
get_facebook_followers(profile_url)
