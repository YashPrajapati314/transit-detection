import requests
from bs4 import BeautifulSoup
import os

URL = "https://www.astrouw.edu.pl/ogle/ogle4/OCVS/blg/transits/phot_ogle4/I/"
response = requests.get(URL)
soup = BeautifulSoup(response.text, 'html.parser')

os.makedirs("light_curves_dat", exist_ok=True)

for link in soup.find_all('a'):
    href = link.get('href')
    if href.endswith('.dat'):
        file_url = URL + href
        print(f"Downloading {file_url}")
        r = requests.get(file_url)
        with open(os.path.join("light_curves_dat", href), 'wb') as f:
            f.write(r.content)
