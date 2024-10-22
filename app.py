from flask import Flask, request, jsonify  
from selenium import webdriver  
from selenium.webdriver.common.by import By  
from selenium.webdriver.chrome.options import Options  
import time  
from flask_cors import CORS 
import re
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains

app = Flask(__name__)  

CORS(app) 
# Initialize Chrome options  
options = Options()  
options.add_argument("--headless")  


def get_facebook_followers(profile_url):  
    # Start the WebDriver  
    driver = webdriver.Chrome(options=options)  
    followers_count = None  
    
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
    
    return followers_count  

def get_twitter_followers(profile_url):
    driver = webdriver.Chrome(options=options)
    followers_count = None

    try:
        # Open the profile URL
        driver.get(profile_url)
        time.sleep(3)  # Wait for the profile page to load

        # Locate the element containing the followers count
        followers_element = driver.find_element(By.CLASS_NAME, 'css-175oi2r')

        # Extract the text from the followers element
        spans = followers_element.find_elements(By.TAG_NAME, 'span')

        # Initialize variable to store follower count

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

    return followers_count  

def get_instagram_followers(profile_url):
    driver = webdriver.Chrome(options=options)
    followers_count = None
    try:

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
    except Exception as e:
            print(f"Error: {e}")

    finally:
        driver.quit()

    return followers_count  
  
def get_youtube_followers(profile_url):
    driver = webdriver.Chrome(options=options)
    followers_count = None
    try:
        # Open the YouTube channel URL
        driver.get(profile_url)
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
            followers_count = count_with_suffix
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

    return followers_count

def get_snapchat_followers(profile_url):
    driver = webdriver.Chrome(options=options)
    followers_count = 0
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
                followers_count = subscribers_count
                print(f"Subscribers Count: {subscribers_count}")
            else:
                print("Subscribers element not found.")
        
        except Exception as e:
            print(f"Error extracting subscribers count: {e}")
    
    finally:
        # Close the browser
        driver.quit()
    return followers_count

def get_linkedin_followers(profile_url):
    driver = webdriver.Chrome(options=options)
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
        return 0


@app.route('/social/api/get_facebook_followers', methods=['POST'])  
def get_followers():  
    data = request.get_json()  
    
    # Validate input data  
    if 'profile_url' not in data:  
        return jsonify({'error': 'Profile URL is required.'}), 400  

    profile_url = data['profile_url']  
    
    followers_count = get_facebook_followers(profile_url)  
    
    if followers_count is None:  
        return jsonify({'error': 'Could not retrieve followers count.'}), 500  
    
    return jsonify({'followers_count': followers_count})  

@app.route('/social/api/get_twitter_followers', methods=['POST'])  
def get_twitter_followers_api():  
    data = request.get_json()  
    
    # Validate input data  
    if 'profile_url' not in data:  
        return jsonify({'error': 'Profile URL is required.'}), 400  

    profile_url = data['profile_url']  
    
    followers_count = get_twitter_followers(profile_url)  
    
    if followers_count is None:  
        return jsonify({'error': 'Could not retrieve followers count.'}), 500  
    
    return jsonify({'followers_count': followers_count})  

@app.route('/social/api/get_instagram_followers', methods=['POST'])  
def get_instagram_followers_api():  
    data = request.get_json()  
    
    # Validate input data  
    if 'profile_url' not in data:  
        return jsonify({'error': 'Profile URL is required.'}), 400  

    profile_url = data['profile_url']  
    
    followers_count = get_instagram_followers(profile_url)  
    
    if followers_count is None:  
        return jsonify({'error': 'Could not retrieve followers count.'}), 500  
    
    return jsonify({'followers_count': followers_count})  

@app.route('/social/api/get_youtube_followers', methods=['POST'])  
def get_youtube_followers_api():  
    data = request.get_json()  
    
    # Validate input data  
    if 'profile_url' not in data:  
        return jsonify({'error': 'Profile URL is required.'}), 400  

    profile_url = data['profile_url']  
    
    followers_count = get_youtube_followers(profile_url)  
    
    if followers_count is None:  
        return jsonify({'error': 'Could not retrieve followers count.'}), 500  
    
    return jsonify({'followers_count': followers_count})  

@app.route('/social/api/get_snapchat_followers', methods=['POST'])  
def get_snapchat_followers_api():  
    data = request.get_json()  
    
    # Validate input data  
    if 'profile_url' not in data:  
        return jsonify({'error': 'Profile URL is required.'}), 400  

    profile_url = data['profile_url']  
    
    followers_count = get_snapchat_followers(profile_url)  
    
    if followers_count is None:  
        return jsonify({'error': 'Could not retrieve followers count.'}), 500  
    
    return jsonify({'followers_count': followers_count})  

@app.route('/social/api/get_linkedin_followers', methods=['POST'])  
def get_linkedin_followers_api():  
    data = request.get_json()  
    
    # Validate input data  
    if 'profile_url' not in data:  
        return jsonify({'error': 'Profile URL is required.'}), 400  

    profile_url = data['profile_url']  
    
    followers_count = get_linkedin_followers(profile_url)  
    
    if followers_count is None:  
        return jsonify({'error': 'Could not retrieve followers count.'}), 500  
    
    return jsonify({'followers_count': followers_count})  

if __name__ == '__main__':  
    app.run(debug=True)