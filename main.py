import requests
from bs4 import BeautifulSoup
import os

RESEND_API_KEY = os.getenv("RESEND_API_KEY")

URL = "https://findajob.dwp.gov.uk/search?q=psychology"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers, timeout=30)

soup = BeautifulSoup(response.text, "html.parser")

jobs_html = ""

keywords = [
    "assistant psychologist",
    "psychological wellbeing practitioner",
    "research assistant",
    "occupational therapy assistant",
    "educational mental health practitioner",
    "children wellbeing practitioner",
    "mental health wellbeing practitioner"
]

locations = [
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

cards = soup.find_all("article")

for card in cards:

    text = card.get_text(" ", strip=True)

    lower = text.lower()

    if any(k in lower for k in keywords):

        if any(loc in lower for loc in locations):

            if "qualified pwp" in lower:
                continue

            if "nurse" in lower:
                continue

            link_tag = card.find("a")

            link = ""

            if link_tag:
                href = link_tag.get("href")

                if href.startswith("/"):
                    link = "https://findajob.dwp.gov.uk" + href
                else:
                    link = href

            jobs_html += f"""
            <p>
            <b>{text}</b><br>
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

print("EMAIL SENT")
