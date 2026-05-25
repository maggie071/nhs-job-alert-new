import requests
from bs4 import BeautifulSoup
import os

RESEND_API_KEY = os.getenv("RESEND_API_KEY")

URL = "https://www.jobs.nhs.uk/candidate/search/results?keyword=assistant+psychologist&location=London"

headers_browser = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers_browser)

print(response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

links = soup.find_all("a")

job_list = []

for link in links:

    text = link.get_text(strip=True)

    href = link.get("href")

    if href and "job_list" in href.lower():

        if "assistant psychologist" in text.lower():

            full_link = "https://www.jobs.nhs.uk" + href

            job_list.append({
                "title": text,
                "link": full_link
            })

html_content = "<h1>New NHS Jobs Found</h1>"

if len(job_list) == 0:

    html_content += "<p>No jobs found.</p>"

else:

    for job in job_list:

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
