import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup

# Initialize Chrome options
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])

# User-Agent to avoid detection
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
options.add_experimental_option('useAutomationExtension', False)
options.add_argument(f'user-agent={user_agent}')

# Initialize the Chrome driver
driver = webdriver.Chrome(options=options)

# Function to extract followers count from a LinkedIn profile
def extract_followers_count(profile_url):
    driver.get(profile_url)
    
    # Wait for the dismiss button to load and click it
    try:
        button = driver.find_element(By.XPATH, "//button[@aria-label='Dismiss']")
        ActionChains(driver).move_to_element(button).click().perform() # Wait for the action to complete
    except Exception as e:
        print("Dismiss button not found or could not be clicked:", e)
        return None

    # Get the page source after clicking
    src = driver.page_source
    soup = BeautifulSoup(src, 'lxml')

    # Find the followers count
    followers_span = soup.find('span', string=lambda text: text and 'followers' in text)
    if followers_span:
        followers_count = followers_span.text.strip()
        return followers_count
    else:
        print("Followers count not found.")
        return None

# Replace this with the actual LinkedIn profile URL
profile_url = "https://www.linkedin.com/in/raghavgupta1604/"
followers_count = extract_followers_count(profile_url)

if followers_count:
    print(f"Followers count: {followers_count}")

# Close the driver
driver.quit()
