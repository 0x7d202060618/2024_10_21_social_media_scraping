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

def extract_subscriber_count(channel_url):
    driver = webdriver.Chrome(options=options)

    try:
        # Open the YouTube channel URL
        driver.get(channel_url)
        time.sleep(3)  # Wait for the page to load

        # Locate the element containing subscriber count
        subscriber_element = driver.find_element(By.XPATH, '//span[contains(@class, "yt-core-attributed-string") and contains(text(), "subscribers")]')

        # Extract the text
        subscriber_text = subscriber_element.text

        # Use regex to extract the numeric value with M or K
        match = re.search(r'(\d+\.?\d*)\s*(M|K)?\s*subscribers', subscriber_text)

        if match:
            count_with_suffix = match.group(1)  # Get the numeric part
            suffix = match.group(2)  # Get the suffix (M or K) if it exists
            
            # Print just the numeric part along with the suffix
            if suffix:
                print(f"Subscribers Count: {count_with_suffix}{suffix}")
            else:
                print(f"Subscribers Count: {count_with_suffix}")  # No suffix if it doesn't exist
        else:
            print("Subscriber count not found.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        driver.quit()

# Example usage:
channel_url = 'https://www.youtube.com/@tseries'  # Replace with the actual channel URL
extract_subscriber_count(channel_url)
