import requests
from bs4 import BeautifulSoup
import os

RESEND_API_KEY = os.getenv("RESEND_API_KEY")

URL = "https://findajob.dwp.gov.uk/search?q=assistant+psychologist&loc=86383"

headers_browser = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers_browser)

soup = BeautifulSoup(response.text, "html.parser")

jobs = soup.find_all("a")

job_list = []

for job in jobs:

    title = job.get_text(strip=True)

    href = job.get("href")

    if href:

        if "assistant psychologist" in title.lower():

            full_link = "https://findajob.dwp.gov.uk" + href

            job_list.append({
                "title": title,
                "link": full_link
            })

html_content = "<h1>New NHS Jobs Found</h1>"

if len(job_list) == 0:

    html_content += "<p>No jobs found.</p>"

else:

    for job in job_list[:10]:

        html_content += f"""
        <p>
        <strong>{job['title']}</strong><br>
        <a href="{job['link']}">{job['link']}</a>
        </p>
        <hr>
        """

headers = {
    "Authorization": f"Bearer {RESEND_API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "from": "onboarding@resend.dev",
    "to": "margaretchai071@gmail.com",
    "subject": "🧠 New Assistant Psychologist Jobs",
    "html": html_content
}

response = requests.post(
    "https://api.resend.com/emails",
    headers=headers,
    json=data
)

print(response.status_code)
print(response.text)
