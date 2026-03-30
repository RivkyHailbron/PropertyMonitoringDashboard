<img width="1823" height="901" alt="image" src="https://github.com/user-attachments/assets/17f2025d-7c7b-4fb0-996b-24d418648b9f" /># Property Compliance and Inspection Monitoring System

## Project Overview
This automated system provides property managers and stakeholders with a high-level executive dashboard to monitor building inspections, complaints, and violations for APN: 2654002037. 

The solution automates data extraction from municipal portals and applies advanced business logic to determine operational statuses based on chronological activity history.

---

## Business Logic and Status Definitions

Since source data lacks explicit status labels, the system analyzes the Activity Flow (Case Stack) to determine the state of each case.

### 1. Status Logic
* NEW: Assigned when the latest activity in the stack is 'Senior Inspector Appeal Received'.
* OPEN: Cases where a complaint was received, but no initial inspection has been performed yet.
* IN PROGRESS: Cases that have reached the 'Site Visit/Initial Inspection' stage and remain active without a closure date.
* CLOSED: Cases with a definitive date recorded in the 'Date Closed' column of the primary record.

### 2. Urgency and Prioritization
Within the In Progress category, the system identifies HIGH urgency cases:
* Logic: If the most recent event (top of the stack) is a 'Compliance Date', the case is flagged as HIGH.
* Assumption: A Compliance Date indicates a mandatory legal deadline. It is assumed that an official follow-up inspection is imminent.
* Sorting: High-priority cases are sorted from the oldest Compliance Date to the newest. 
    * Rationale: Cases that have been waiting the longest since their compliance deadline are statistically more likely to be inspected next.

---

## Technical Features
* Hybrid Scraping Engine: Combined Selenium and Multi-threaded Requests (20 concurrent workers) for high-speed data extraction.
* Data Enrichment: Automatically extracts the "Nature of Complaint" for every case to provide context.
* Executive Dashboard: Built with Streamlit, featuring interactive Plotly charts and deep-dive filtering tabs.

---
## Screen 
### I manually made one in the treatment and it would be urgent-HIGH to see it clearly Screenshot where I made one in the treatment and urgent (HIGH) so we can see it in the charts
<img width="1838" height="850" alt="image" src="https://github.com/user-attachments/assets/f55592cf-f64e-416d-9634-c39132c77c8b" />
### Select a case and see the details:
<img width="1823" height="901" alt="image" src="https://github.com/user-attachments/assets/cbc04a22-6613-4d78-8591-8267097e2902" />
### select:
<img width="1823" height="901" alt="image" src="https://github.com/user-attachments/assets/5ea3078b-2396-4526-b620-db56d54e2b2c" />


## Installation and Execution Guide

### 1. Prerequisites
* Python 3.9 or higher.
* Google Chrome browser installed.

### 2. Quick Start (Windows)
1. Download or clone this repository.
2. Double-click the file: **run_me.bat**
3. The system will automatically install requirements, fetch data, and launch the dashboard.

---

## Future Improvements
* Smart Deduplication: Implementation of logic to identify and merge duplicate complaints.
* Delta Updates: Optimization of the engine to update the database only when changes are detected.
* AI Analysis: Integration of Large Language Models to categorize complaint text and assess risks.

---

## Project Structure
* scraping.py: Orchestrates parallel scraping and case classification.
* selenium_scraping.py: Core utility functions for web extraction.
* app.py: Streamlit dashboard UI and interactive logic.
* requirements.txt: Project dependencies
 
 
