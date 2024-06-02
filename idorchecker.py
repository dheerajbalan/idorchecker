import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urljoin
import argparse
import urllib3
from colorama import Fore

red = Fore.RED
green = Fore.GREEN
yellow = Fore.YELLOW

def get_banner():
    banner = """ 
       ___  ______   _______  ______    __   __  __   __  __    _  _______  _______  ______   
      |   ||      | |       ||    _ |  |  | |  ||  | |  ||  |  | ||       ||       ||    _ |  
      |   ||  _    ||   _   ||   | ||  |  |_|  ||  | |  ||   |_| ||_     _||    ___||   | ||  
      |   || | |   ||  | |  ||   |_||_ |       ||  |_|  ||       |  |   |  |   |___ |   |_||_ 
      |   || |_|   ||  |_|  ||    __  ||       ||       ||  _    |  |   |  |    ___||    __  |
      |   ||       ||       ||   |  | ||   _   ||       || | |   |  |   |  |   |___ |   |  | |
      |___||______| |_______||___|  |_||__| |__||_______||_|  |__|  |___|  |_______||___|  |_|


    """
    print(yellow + banner)

def fetch_page(url):
    """Fetches the content of the page from the given URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_html(html):
    """Parses the HTML content using BeautifulSoup."""
    return BeautifulSoup(html, 'html.parser')

def extract_links(soup, base_url):
    """Extracts all the links from the parsed HTML."""
    links = set()
    for a_tag in soup.find_all('a', href=True):
        link = a_tag['href']
        # Join relative URLs with base URL
        full_link = urljoin(base_url, link)
        links.add(full_link)
    return links

def extract_parameters(url):
    """Extracts the parameters from the given URL."""
    parsed_url = urlparse(url)
    parameters = parse_qs(parsed_url.query)
    return parameters

def payload_wordlists(payload_file):
    with open(payload_file, "r") as f:
        payloads = [line.strip() for line in f]
    return payloads

def idor_Checker(base_url, parameters, payloads):
    print(yellow + f"[*] Checking for any IDOR vulnerability on {base_url}")
    try:
        for param, values in parameters.items():
            for value in values:
                for pay in payloads:
                    modified_url = base_url.replace(f"{param}={value}", f"{param}={pay}")
                    response = requests.get(modified_url)
                    if response.status_code == 200:
                        if potential_idor_check(response.text):
                            print(green + f"[+] IDOR vulnerability found: {modified_url} (200)")
                        else:
                            print(red + f"[-] No sensitive data exposed: {modified_url} (404)")
                    elif response.status_code == 404:
                        print(red + f"[-] No IDOR vulnerability found: {modified_url} (404)")
    except requests.exceptions.ConnectionError:
        print(yellow,"[!] Connection error occurred.")
    except urllib3.exceptions.ProtocolError:
        print(yellow,"[!] Protocol error occurred.")
    except ConnectionResetError:
        print(yellow,"[!] Connection reset error occurred.")

def potential_idor_check(response_text):
    keys = ["user_data", "admin panel", "restricted access"]
    for data in keys:
        if data in response_text.lower():
            print(green + f"[DEBUG] Sensitive data has been exposed: {data}")
            return True
    print(red + "[-] No sensitive data exposed.")
    return False

def main(start_url, payload_file):
    if not start_url.startswith(('http://', 'https://')):
        start_url = 'https://' + start_url
    html_content = fetch_page(start_url)
    if html_content is None:
        return

    soup = parse_html(html_content)
    base_url = "{0.scheme}://{0.netloc}{0.path}".format(urlparse(start_url))
    links = extract_links(soup, base_url)
    payloads = payload_wordlists(payload_file)

    for link in links:
        params = extract_parameters(link)
        if params:
            idor_Checker(link, params, payloads)

def get_arguments():
    parser = argparse.ArgumentParser(description='Web scraper for extracting parameters from URLs and checking IDOR vulnerabilities.')
    parser.add_argument('-u', '--url', type=str, help='URL of the website to scrape')
    parser.add_argument('-p', '--payload_file', type=str, help='File containing payload wordlists')
    return parser.parse_args()
    
get_banner()
args = get_arguments()
try:
    url = args.url
    payload_file = args.payload_file

    if url and payload_file:
        main(url, payload_file)
    else:
        print(yellow + "[!] Both URL and payload file are required.")
except KeyboardInterrupt:
    print("\n CTRL + C has been clicked, Exiting....")