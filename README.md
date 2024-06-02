IDOR Checker Tool

IODRHunter is an IDOR (Insecure Direct Object Reference) checker tool built with Python. The tool scrapes a given URL for links, extracts the parameters from those links, and checks for potential IDOR vulnerabilities using payloads from a specified wordlist.

 Features

- Fetches the content of a webpage.
- Parses HTML to extract all links.
- Extracts URL parameters.
- Checks for potential IDOR vulnerabilities using a wordlist of payloads.
- Identifies and reports any sensitive data exposure.

 Requirements

- Python 3.x
- `requests` library
- `beautifulsoup4` library
- `colorama` library
- `urllib3` library

## Installation

1. Clone the repository or download the script file.
2. Install the required Python packages using `pip`:

bash
	pip install requests beautifulsoup4 colorama urllib3

Usage

To run the IDOR checker, use the following command:

bash

	python3 idor_checker.py -u <URL> -p <payload_file>

Replace <URL> with the target URL you want to scan and <payload_file> with the path to your payload wordlist file.
Example Command

bash

	python3 idor_checker.py -u https://example.com -p payloads.txt

Example Output

less

-----------------------------------------
       ___  ______   _______  ______    __   __  __   __  __    _  _______  _______  ______   
      |   ||      | |       ||    _ |  |  | |  ||  | |  ||  |  | ||       ||       ||    _ |  
      |   ||  _    ||   _   ||   | ||  |  |_|  ||  | |  ||   |_| ||_     _||    ___||   | ||  
      |   || | |   ||  | |  ||   |_||_ |       ||  |_|  ||       |  |   |  |   |___ |   |_||_ 
      |   || |_|   ||  |_|  ||    __  ||       ||       ||  _    |  |   |  |    ___||    __  |
      |   ||       ||       ||   |  | ||   _   ||       || | |   |  |   |  |   |___ |   |  | |
      |___||______| |_______||___|  |_||__| |__||_______||_|  |__|  |___|  |_______||___|  |_|


[*] Checking for any IDOR vulnerability on https://example.com
[+] IDOR vulnerability found: https://example.com/path?param=payload (200)
[-] No sensitive data exposed: https://example.com/path?param=payload (404)



License

This project is licensed under the MIT License. See the LICENSE file for details.
Acknowledgments

    This tool uses the requests and beautifulsoup4 libraries for web scraping.
    Inspired by various web security and penetration testing scripts and tutorials.
