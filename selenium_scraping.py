import os
import ssl
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Global SSL bypass for requests
ssl._create_default_https_context = ssl._create_unverified_context
os.environ['WDM_SSL_VERIFY'] = '0'


def start_driver():
    """Start an optimized headless Chrome driver without images."""
    options = Options()
    options.add_argument("--headless")  # Run Chrome in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument('--blink-settings=imagesEnabled=false')  # Disable images for faster performance

    service = Service(ChromeDriverManager().install())  # Automatically install the correct version of ChromeDriver
    return webdriver.Chrome(service=service, options=options)


def get_case_flow_fast(case_url):
    """Fetch complaint history and nature using fast Requests."""
    flow = []
    nature = "Not Specified"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        # Short timeout (10 seconds) for faster scraping
        response = requests.get(case_url, verify=False, timeout=10, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract Nature of Complaint
            full_text = soup.get_text(separator=" ")
            if "Nature of Complaint:" in full_text:
                nature_part = full_text.split("Nature of Complaint:")[1]
                nature = nature_part.split("Date")[0].strip()
                nature = " ".join(nature.split())

            # Extract activity history (flow)
            tables = soup.find_all('table')
            target_table = None
            for t in tables:
                if "Activity" in t.get_text():
                    target_table = t
                    break

            if target_table:
                rows = target_table.find_all('tr')
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 2:
                        d_txt = cells[0].get_text(strip=True)
                        a_txt = cells[1].get_text(strip=True)
                        if d_txt and a_txt and d_txt.lower() != "date":
                            flow.append({"date": d_txt, "activity": a_txt})

        flow.reverse()  # Reverse to get chronological order
    except Exception as e:
        print(f"Error: {e}")
        pass

    return flow, nature