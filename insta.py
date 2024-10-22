import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

# Initialize Chrome options
options = Options()
# options.add_argument("--headless")  # Uncomment if you want headless mode
options.add_argument("start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
options.add_experimental_option('useAutomationExtension', False)
options.add_argument(f'user-agent={user_agent}')
driver = webdriver.Chrome(options=options)

# Ask for the LinkedIn profile URL
profile_url = "https://www.instagram.com/virat.kohli/"

# Open the provided URL
driver.get(profile_url)

# Wait for the page to load
time.sleep(3)

# Dismiss any popup/modal
try:
    button = driver.find_element(By.XPATH, "//div[contains(@class, 'x1i10hfl') and contains(@class, 'x1y1aw1k')]")
    ActionChains(driver).move_to_element(button).click().perform()
except Exception as e:
    print("No popup found or could not dismiss it:", e)

# Use a CSS selector to find the span element with the title attribute
followers_span = driver.find_element(By.CSS_SELECTOR, "span.x5n08af.x1s688f[title]")
followers_count = followers_span.get_attribute("title")
print(f"Followers count: {followers_count}")

# Close the WebDriver
driver.quit()
