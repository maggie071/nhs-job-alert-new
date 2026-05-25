import requests
from bs4 import BeautifulSoup
import os

# =========================
# RESEND CONFIG
# =========================

RESEND_API_KEY = os.getenv("RESEND_API_KEY")

# =========================
# SEARCH URL
# =========================

URL = "https://www.jobs.nhs.uk/candidate/search/results?keyword=assistant+psychologist&location=London"

# =========================
# GET NHS JOBS
# =========================

response = requests.get(URL)

soup = BeautifulSoup(response.text, "html.parser")

jobs = soup.find_all("a", class_="nhsuk-link")

job_list = []

for job in jobs[:10]:

    title = job.get_text(strip=True)

    link = "https://www.jobs.nhs.uk" + job.get("href")

    if "assistant psychologist" in title.lower():

        job_list.append({
            "title": title,
            "link": link
        })

# =========================
# BUILD EMAIL
# =========================

html_content = "<h1>New NHS Jobs Found</h1>"

for job in job_list:

    html_content += f"""
    <p>
    <strong>{job['title']}</strong><br>
    <a href="{job['link']}">{job['link']}</a>
    </p>
    <hr>
    """

# =========================
# SEND EMAIL
# =========================

headers = {
    "Authorization": f"Bearer {RESEND_API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "from": "onboarding@resend.dev",
    "to": "margaretchai071@gmail.com",
    "subject": "🧠 New NHS Assistant Psychologist Jobs",
    "html": html_content
}

response = requests.post(
    "https://api.resend.com/emails",
    headers=headers,
    json=data
)

print(response.status_code)
print(response.text)
