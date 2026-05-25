import requests
from bs4 import BeautifulSoup
import os

SERPAPI_KEY = os.getenv("SERPAPI_KEY")
RESEND_API_KEY = os.getenv("RESEND_API_KEY")

keywords = [
    "Assistant Psychologist NHS",
    "Trainee Psychological Wellbeing Practitioner NHS",
    "Research Assistant Mental Health NHS",
    "Occupational Therapy Assistant NHS",
    "Educational Mental Health Practitioner NHS",
    "Children Wellbeing Practitioner NHS"
]

locations = [
    "London",
    "Greater London",
    "Oxford",
    "Cambridge",
    "Manchester",
    "Leeds",
    "York",
    "Nottingham",
    "Exeter"
]

all_jobs = []

for keyword in keywords:
    for location in locations:

        params = {
            "engine": "google_jobs",
            "q": f"{keyword} {location}",
            "api_key": SERPAPI_KEY
        }

        response = requests.get(
            "https://serpapi.com/search",
            params=params,
            timeout=30
        )

        data = response.json()

        jobs = data.get("jobs_results", [])

        for job in jobs:

            title = job.get("title", "")
            company = job.get("company_name", "")
            loc = job.get("location", "")
            link = job.get("related_links", [{}])[0].get("link", "")

            lower_title = title.lower()

            if (
                "qualified pwp" in lower_title
                or "nurse" in lower_title
            ):
                continue

            all_jobs.append(
                f"""
                <p>
                <b>{title}</b><br>
                {company}<br>
                {loc}<br>
                <a href="{link}">View Job</a>
                </p>
                <hr>
                """
            )

if not all_jobs:
    html_content = "<h1>No matching jobs found.</h1>"
else:
    html_content = "".join(all_jobs[:30])

email_data = {
    "from": "onboarding@resend.dev",
    "to": "maggieee1213@gmail.com",
    "subject": "🧠 New NHS Mental Health Jobs",
    "html": html_content
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
