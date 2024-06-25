# Brutelenium - Bruteforce using Selenium

This script automates bruteforce attacks using Selenium. It supports usernames and passwords from strings or wordlists, proxy configuration, target URL, and customizable sleep time. This can be useful for security testing and automation purposes.

## Features

- Supports single username/password or wordlists for brute force testing.
- Optional proxy configuration with URL and port.
- Customizable target URL for the login page.
- Adjustable sleep time between actions.

## Usage

```sh
python script.py -t TARGET_URL [-u USERNAME | -U USERLIST] [-p PASSWORD | -P PASSLIST] [--proxy PROXY] [-s SLEEP_TIME]
```

### Options

- `-u, --username`: Username for login (optional if `-U` is used).
- `-p, --password`: Password for login (optional if `-P` is used).
- `-U, --userlist`: Path to a file containing a list of usernames (optional if `-u` is used).
- `-P, --passlist`: Path to a file containing a list of passwords (optional if `-p` is used).
- `--proxy`: Proxy URL and port (optional).
- `-t, --target`: Target URL for the login page (required).
- `-s, --sleep-time`: Sleep time between actions in milliseconds (default is 3000 ms).

### Example

```sh
python script.py -t http://192.168.1.1/login -u admin -P /path/to/passwords.txt --proxy 127.0.0.1:8080 -s 500
```

## Requirements

- Python 3.x
- Selenium
- Chrome WebDriver

## Installation

1. Clone the repository:
    ```sh
    git clone git@github.com:Astaruf/Brutelenium.git
    cd Brutelenium
    ```

2. Install the required Python packages:
    ```sh
    python3 -m pip install selenium
    ```

3. Download and place the Chrome WebDriver in your PATH:
    - [ChromeDriver Download](https://sites.google.com/a/chromium.org/chromedriver/downloads)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This script is intended for educational and testing purposes only. Use it responsibly and do not use it to attack systems without permission.
Feel free to customize the repository URL and other details as needed.
