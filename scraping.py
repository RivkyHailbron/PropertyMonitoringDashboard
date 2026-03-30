import json
import time
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_scraping import start_driver, get_case_flow_fast

# Function to classify the status of a case
def classify_case(case):
    """Updated status logic: Under treatment from initial inspection."""
    flow = case.get('flow', [])
    # Default: Open (Complaint received but not yet inspected)
    case.update({"status": "Open", "urgency": "LOW"})

    # 1. Closed: If there is a closing date in the main table
    if case['closed_raw'] and case['closed_raw'].strip() != "":
        case.update({"status": "Closed", "urgency": "NULL"})
        return case

    if not flow:
        return case

    last_event = flow[-1]['activity']
    all_acts_upper = [f['activity'].upper() for f in flow]

    # 2. New: If the last event is "SENIOR INSPECTOR APPEAL RECEIVED"
    if "SENIOR INSPECTOR APPEAL RECEIVED" in last_event.upper():
        case.update({"status": "New", "urgency": "NULL"})

    # 3. In Progress: From Initial Inspection to Closure
    elif "SITE VISIT/INITIAL INSPECTION" in str(all_acts_upper):
        case.update({"status": "In Progress"})
        # High urgency if last event is Compliance Date
        case['urgency'] = "HIGH" if "COMPLIANCE DATE" in last_event.upper() else "LOW"

    # 4. Open: Complaint exists but hasn't reached Initial Inspection
    else:
        case.update({"status": "Open", "urgency": "LOW"})

    return case

# Function to run the scraping process
def run_scraper():
    apn = "2654002037"
    driver = start_driver()
    url = f"https://housingapp.lacity.org/reportviolation/Pages/PropAtivityCases?APN={apn}&Source=ActivityReport"

    print(f"🌐 Fetching cases for APN {apn}...")
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)
        select = Select(wait.until(EC.presence_of_element_located((By.NAME, "dgPropCases2_length"))))
        select.select_by_value("-1")
        time.sleep(5)

        rows = driver.find_elements(By.XPATH, "//table[@id='dgPropCases2']/tbody/tr")
        cases_to_process = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 4:
                c_type, c_num, c_closed = cells[1].text, cells[2].text, cells[3].text
                t_id = "1" if "Complaint" in c_type else "2" if "Systematic" in c_type else "3"
                d_url = f"https://housingapp.lacity.org/reportviolation/Pages/PublicPropertyActivityReport?APN={apn}&CaseType={t_id}&CaseNo={c_num}"
                cases_to_process.append(
                    {"case_type": c_type, "case_number": c_num, "closed_raw": c_closed, "url": d_url})

        driver.quit()
        print(f"🚀 Processing {len(cases_to_process)} cases in parallel...")

        # Function to fetch case details in parallel
        def fetch_worker(c):
            f, n = get_case_flow_fast(c['url'])
            c['flow'], c['complaint_nature'] = f, n
            return classify_case(c)

        # Using ThreadPoolExecutor for parallel processing
        with ThreadPoolExecutor(max_workers=20) as executor:
            results = list(executor.map(fetch_worker, cases_to_process))

        # Save results to JSON file
        with open("inspections_data.json", "w", encoding="utf-8") as f:
            json.dump({"inspections": results}, f, indent=4, ensure_ascii=False)
        print("🏁 Done!")

    except Exception as e:
        print(f"❌ Error: {e}")
        if 'driver' in locals(): driver.quit()

# Execute the scraper
if __name__ == "__main__":
    run_scraper()