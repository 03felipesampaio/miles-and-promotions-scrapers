# miles-and-promotions-scrapers
A set of webscrapers to gather discounts by miles clubs and cashbacks

## Motivation
I was tired of checking many websites daily to track the cashback and miles offered by each one. To save time and effort, I decided to automate these visits. These crawlers visit the websites daily, retrieve the content of the pages, and extract the relevant information, which is then stored in a PostgreSQL database.

## Technology Stack
- **Python**: Used for scripting the crawlers.
- **httpx**: For performing HTTP requests.
- **Google Cloud Platform (GCP)**:
  - **Cloud Storage**: To store the page responses.
  - **Cloud Run Jobs**: To run the crawlers.
- **Airflow**: To orchestrate and schedule the jobs.

## Current Scope
Currently, the crawlers are tracking the following websites:
- Livelo
- Inter Shop
- Esfera
- Nubank Shop
