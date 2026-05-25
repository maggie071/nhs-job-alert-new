import requests
from bs4 import BeautifulSoup
import os

RESEND_API_KEY = os.getenv("RESEND_API_KEY")

RSS_URL = "https://findajob.dwp.gov.uk/rss?keywords=assistant+psychologist&location=London"

response = requests.get(RSS_URL)

soup = BeautifulSoup(response.content, "xml")

items = soup.find_all("item")

html_content = "<h1>New Assistant Psychologist Jobs</h1>"

if len(items) == 0:

    html_content += "<p>No jobs found.</p>"

else:

    for item in items[:10]:

        title = item.title.text
        link = item.link.text

        html_content += f"""
        <p>
        <strong>{title}</strong><br>
        <a href="{link}">{link}</a>
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
