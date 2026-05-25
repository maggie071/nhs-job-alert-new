import requests
from bs4 import BeautifulSoup
import os

RESEND_API_KEY = os.getenv("RESEND_API_KEY")

search_urls = [
    "https://www.jobs.nhs.uk/candidate/search/results?keyword=assistant+psychologist",
    "https://www.jobs.nhs.uk/candidate/search/results?keyword=trainee+psychological+wellbeing+practitioner",
    "https://www.jobs.nhs.uk/candidate/search/results?keyword=research+assistant+mental+health",
    "https://www.jobs.nhs.uk/candidate/search/results?keyword=occupational+therapy+assistant",
    "https://www.jobs.nhs.uk/candidate/search/results?keyword=educational+mental+health+practitioner",
]

allowed_locations = [
    "london",
    "greater london",
    "oxford",
    "cambridge",
    "manchester",
    "leeds",
    "york",
    "nottingham",
    "exeter"
]

jobs_html = ""

headers = {
    "User-Agent": "Mozilla/5.0"
}

for url in search_urls:

    response = requests.get(url, headers=headers, timeout=30)

    soup = BeautifulSoup(response.text, "html.parser")

    jobs = soup.find_all("li", class_="search-result")

    for job in jobs:

        title_tag = job.find("h2")

        if not title_tag:
            continue

        title = title_tag.get_text(strip=True)

        lower_title = title.lower()

        if "qualified pwp" in lower_title or "nurse" in lower_title:
            continue

        location_tag = job.find("li", class_="search-result__location")

        location = ""

        if location_tag:
            location = location_tag.get_text(strip=True)

        location_lower = location.lower()

        if not any(loc in location_lower for loc in allowed_locations):
            continue

        link_tag = title_tag.find("a")

        link = ""

        if link_tag:
            link = "https://www.jobs.nhs.uk" + link_tag.get("href")

        jobs_html += f"""
        <p>
        <b>{title}</b><br>
        {location}<br>
        <a href="{link}">View Job</a>
        </p>
        <hr>
        """

if jobs_html == "":
    jobs_html = "<h2>No matching jobs found.</h2>"

email_data = {
    "from": "onboarding@resend.dev",
    "to": "margaretchai071@gmail.com",
    "subject": "🧠 New NHS Mental Health Jobs",
    "html": jobs_html
}

requests.post(
    "https://api.resend.com/emails",
    headers={
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    },
    json=email_data
)

print("Email sent successfully")
