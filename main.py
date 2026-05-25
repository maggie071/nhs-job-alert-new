import requests
import os
from bs4 import BeautifulSoup

RESEND_API_KEY = os.getenv("RESEND_API_KEY")

RSS_URL = "https://www.jobs.nhs.uk/api/search?keyword=assistant+psychologist&location=London&distance=10&format=rss"

response = requests.get(
    RSS_URL,
    headers={
        "User-Agent": "Mozilla/5.0"
    },
    timeout=30
)

soup = BeautifulSoup(response.content, "xml")

items = soup.find_all("item")[:10]

job_list = ""

for item in items:
    title = item.title.text
    link = item.link.text

    job_list += f"""
    <p>
        <strong>{title}</strong><br>
        <a href="{link}">View Job</a>
    </p>
    <hr>
    """

if not job_list:
    job_list = "<p>No jobs found.</p>"

url = "https://api.resend.com/emails"

headers = {
    "Authorization": f"Bearer {RESEND_API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "from": "onboarding@resend.dev",
    "to": "你的邮箱@gmail.com",
    "subject": "🧠 New Assistant Psychologist Jobs",
    "html": f"""
    <h1>New Assistant Psychologist Jobs</h1>
    {job_list}
    """
}

response = requests.post(
    url,
    headers=headers,
    json=data
)

print(response.status_code)
print(response.text)
