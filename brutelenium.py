import time
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def main():
    parser = argparse.ArgumentParser(description="Automated login script using Selenium")
    parser.add_argument('-u', '--username', type=str, help="Username for login")
    parser.add_argument('-p', '--password', type=str, help="Password for login")
    parser.add_argument('-U', '--userlist', type=str, help="Path to username wordlist")
    parser.add_argument('-P', '--passlist', type=str, help="Path to password wordlist")
    parser.add_argument('--proxy', type=str, help="Proxy URL and port")
    parser.add_argument('-t', '--target', type=str, required=True, help="Target URL for login")
    parser.add_argument('-s', '--sleep-time', type=int, default=3000, help="Sleep time in milliseconds")

    args = parser.parse_args()

    if not (args.username or args.userlist):
        parser.error("Either -u or -U must be specified.")
    if not (args.password or args.passlist):
        parser.error("Either -p or -P must be specified.")

    # Convert sleep time from milliseconds to seconds
    sleep_time = args.sleep_time / 1000.0

    chrome_options = Options()
    if args.proxy:
        chrome_options.add_argument('--proxy-server=%s' % args.proxy)
        chrome_options.add_argument('--ignore-certificate-errors')

    # Create a new Selenium WebDriver instance
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(args.target)

    time.sleep(sleep_time)

    if args.username:
        usernames = [args.username]
    else:
        with open(args.userlist) as f:
            usernames = f.read().splitlines()

    if args.password:
        passwords = [args.password]
    else:
        with open(args.passlist) as f:
            passwords = f.read().splitlines()

    for user in usernames:
        username = driver.find_element(By.XPATH, "//input[@id='username']")
        username.clear()
        username.send_keys(user)
        
        for pwd in passwords:
            password = driver.find_element(By.XPATH, "//input[@id='userpassword']")
            password.clear()
            password.send_keys(pwd)
            button = driver.find_element(By.XPATH, "//*[text()='Entra']")
            # button.click()
            time.sleep(0.5)

    # Close the Selenium WebDriver instance
    driver.quit()

if __name__ == "__main__":
    main()
