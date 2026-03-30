# Property Compliance and Inspection Monitoring System - APN: 2654002037

## Project Overview
This automated system provides property managers and stakeholders with a high-level executive dashboard to monitor building inspections, complaints, and violations for APN: 2654002037. 

The solution automates data extraction from municipal portals and applies advanced business logic to determine operational statuses based on chronological activity history.

---

## Business Logic and Status Definitions

### Understanding the Need
During the data investigation phase, I realized that the raw municipal records lack clear, real-time status labels. To solve this, I decided on the following status logic based on the chronological "Activity Flow" of each case:

* **NEW**: Assigned when the latest activity is 'Senior Inspector Appeal Received', indicating a recent escalation.
* **OPEN**: Cases where a complaint was received, but no initial inspection has been performed yet.
* **IN PROGRESS**: Cases that have reached the 'Site Visit/Initial Inspection' stage and remain active without a closure date.
* **CLOSED**: Cases with a definitive date recorded in the 'Date Closed' column.

### Urgency and Prioritization
Within the **In Progress** category, the system identifies **HIGH** urgency cases:
* **Logic**: If the most recent event is a 'Compliance Date', the case is flagged as HIGH.
* **Assumption**: A Compliance Date indicates a mandatory legal deadline; therefore, a follow-up inspection is imminent.
* **Sorting**: High-priority cases are sorted from the oldest Compliance Date to the newest (Longest waiting = Highest risk).

---

## Data Schema: Selected Fields & Rationale
I chose to extract and store the following fields to ensure maximum operational value:
* **Case Number & Type**: Essential for unique identification and legal classification.
* **Status & Urgency (Derived)**: Created to transform static logs into an actionable management tool.
* **Nature of Complaint**: Automatically enriched to provide immediate context without requiring manual lookups.
* **Activity Flow**: Stored as a full list to allow deep-dive analysis of a case's history directly from the dashboard.

---

## Dashboard Preview

### Executive Overview (High Urgency Tracking)
Manual verification of an "In Progress" case with "HIGH" urgency:
<img width="1838" height="850" alt="image" src="https://github.com/user-attachments/assets/f55592cf-f64e-416d-9634-c39132c77c8b" />

### Interactive Case Selection
Selecting a specific case to view detailed history and complaint nature:
<img width="1858" height="718" alt="image" src="https://github.com/user-attachments/assets/38f41a98-c7d4-4c15-9cf7-77cb0007fad3" />

### Detailed Activity Stack
<img width="1823" height="901" alt="image" src="https://github.com/user-attachments/assets/5ea3078b-2396-4526-b620-db56d54e2b2c" />

---

## Technical Features
* **Hybrid Scraping Engine**: Combined Selenium and Multi-threaded Requests (20 concurrent workers) for high-speed data extraction.
* **Data Enrichment**: Automatic extraction of the "Nature of Complaint" for every case.
* **Executive Dashboard**: Built with Streamlit, featuring interactive Plotly charts.

---

## Installation and Execution Guide

### 1. Prerequisites
* Python 3.9 or higher.
* Google Chrome browser installed.

### 2. Quick Start (Windows)
1. Download or clone this repository.
2. Double-click the file: **run_me.bat**
3. The system will automatically install requirements, fetch data, and launch the dashboard.

---

## Future Improvements & Ideal Tech Stack

### Improvements if given more time:
* **Smart Deduplication**: Implement fuzzy-matching to merge duplicate complaints for the same physical issue.
* **Delta Updates**: Optimize the engine to update only modified records instead of full database rewrites.
* **AI Risk Scoring**: Integrate LLMs to analyze complaint text and automatically categorize severity.

### The Ideal Stack for Scalability:
* **Backend**: **FastAPI** with **PostgreSQL** for robust data persistence.
* **Task Management**: **Celery & Redis** to handle background scraping at scale.
* **Frontend**: **React** for a more flexible, enterprise-grade user interface.

---

## Project Structure
* `scraping.py`: Orchestrates parallel scraping and business logic.
* `selenium_scraping.py`: Core utility functions for web extraction.
* `app.py`: Streamlit dashboard UI and interactive logic.
* `requirements.txt`: Project dependencies.
