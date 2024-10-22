import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Initialize Chrome options
options = Options()
options.add_argument("start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])

def main(profile_url):
    driver = webdriver.Chrome(options=options)

    try:
        # Open the profile URL
        driver.get(profile_url)
        time.sleep(3)  # Wait for the profile page to load

        # Locate the element containing the followers count
        followers_element = driver.find_element(By.CLASS_NAME, 'css-175oi2r')

        # Extract the text from the followers element
        spans = followers_element.find_elements(By.TAG_NAME, 'span')

        # Initialize variable to store follower count
        followers_count = None

        # Iterate through the span elements
        for span in spans:
            text = span.text
            # Use regex to match the follower count format (e.g., '52.6M')
            if re.match(r'^\d+(\.\d+)?[MK]$', text):
                followers_count = text
                break  # Break once we find the follower count

        if followers_count:
            print(f"Followers Count: {followers_count}")
        else:
            print("Followers count not found.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        driver.quit()

# Example usage:
profile_url = 'https://x.com/ChampionsLeague'  # Example profile URL
main(profile_url)
