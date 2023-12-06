import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from queue import Queue
import time
import re


start_url = 'https://www.soccerstats.com/latest.asp?league=england'
base_url = 'https://www.soccerstats.com/latest.asp?league=england'


all_links = set()


processed_urls = set()


queue = Queue()
queue.put(start_url)


start_time = time.time()



html_file_name = "England.txt"
url_file_name = "England_processed_urls.txt"


pattern = r'https://www\.soccerstats\.com/.*league=england.*'


regex = re.compile(pattern)


while not queue.empty():
    current_url = queue.get()


    try:
        if current_url not in processed_urls:
            response = requests.get(current_url)
            if response.status_code == 200:

                soup = BeautifulSoup(response.text, 'html.parser')

                with open(html_file_name, "a", encoding="utf-8") as file:
                    file.write(soup.prettify())


                with open(url_file_name, "a", encoding="utf-8") as url_file:
                    url_file.write(current_url + '\n')


                for link in soup.find_all('a'):
                    href = link.get('href')
                    if href:
                        absolute_url = urljoin(base_url, href)


                        if regex.search(absolute_url):
                            all_links.add(absolute_url)
                            queue.put(absolute_url)


                processed_urls.add(current_url)

    except Exception as e:
        print(f"Error processing {current_url}: {e}")
