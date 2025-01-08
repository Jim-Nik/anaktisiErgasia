import pandas as pd
import requests
from bs4 import BeautifulSoup

response = requests.get("https://en.wikipedia.org/wiki/Giannis_Antetokounmpo")
soup = BeautifulSoup(response.text, 'html.parser')
paragraphs = soup.find_all('p')
parsed_paragraph = [p.text.strip() for p in paragraphs]

try:
    response = requests.get("https://en.wikipedia.org/wiki/Giannis_Antetokounmpo")
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
except requests.RequestException as e:
    print(f"Request failed: {e}")

data = [{'Paragraph': paragraph} for paragraph in parsed_paragraph]
df = pd.DataFrame(data)
df.to_csv('giannis_data.csv', index=False, encoding='utf-8')

