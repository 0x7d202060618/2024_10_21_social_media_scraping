import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Initialize Chrome options
options = Options()
options.add_argument("--headless")
options.add_argument("start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])

# Option to use a custom user-agent
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
options.add_argument(f'user-agent={user_agent}')
options.add_experimental_option('useAutomationExtension', False)

# Function to extract subscriber count
def get_subscriber_count(profile_url):
    driver = webdriver.Chrome(options=options)
    
    try:
        # Open the provided URL
        driver.get(profile_url)
        time.sleep(2)  # Allow time for the page to load
        
        # Get the page source and parse with BeautifulSoup
        src = driver.page_source
        soup = BeautifulSoup(src, 'lxml')

        # Find the subscriber count using the class or data-testid
        try:
            subscriber_element = soup.find('div', {'data-testid': 'subscribersCountText'})
            if subscriber_element:
                subscribers_count = subscriber_element.text.strip()  # Get the text (e.g., "129k Subscribers")
                print(f"Subscribers Count: {subscribers_count}")
            else:
                print("Subscribers element not found.")
        
        except Exception as e:
            print(f"Error extracting subscribers count: {e}")
    
    finally:
        # Close the browser
        driver.quit()

# Ask for the profile URL
profile_url = "https://www.snapchat.com/add/viratk244268"
get_subscriber_count(profile_url)
